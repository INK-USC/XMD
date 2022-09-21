# Basics

## Multirun
Do grid search over different configs.
```
python main.py -m \
    dataset=sst,sst5,stf \
    seed=0,1,2,3,4,5 \
```

## Evaluate checkpoint
This command evaluates a checkpoint on the train, dev, and test sets.
```
python main.py \
    training=evaluate \
    training.ckpt_path=/path/to/ckpt \
    training.eval_splits=train,dev,test \
```

## Fine-tune checkpoint
```
python main.py \
    training=evaluate \
    training.ckpt_path=/path/to/ckpt \
```

## Offline mode
In offline mode, results are not logged to Neptune.
```
python main.py logger.offline=True
```

## Debug mode
In debug mode, results are not logged to Neptune, and we only train/evaluate for limited number of batches and/or epochs.
```
python main.py debug=True
```

## Hydra working directory

Hydra will change the working directory to the path specified in `configs/hydra/default.yaml`. Therefore, if you save a file to the path `'./file.txt'`, it will actually save the file to somewhere like `logs/runs/xxxx/file.txt`. This is helpful when you want to version control your saved files, but not if you want to save to a global directory. There are two methods to get the "actual" working directory:

1. Use `hydra.utils.get_original_cwd` function call
2. Use `cfg.work_dir`. To use this in the config, can do something like `"${data_dir}/${.dataset}/${model.arch}/"`


## Config Key

- `work_dir` current working directory (where `src/` is)

- `data_dir` where data folder is

- `log_dir` where log folder is (runs & multirun)

- `root_dir` where the saved ckpt & hydra config are


---


# Example Commands

Here, we assume the following: 
- The `data_dir` is `../data`, which means `data_dir=${work_dir}/../data`.
- The dataset is `sst`.
- The attribution algorithm is `input-x-gradient`.

## 1. Build dataset
The commands below are used to build pre-processed datasets, saved as pickle files. The model architecture is specified so that we can use the correct tokenizer for pre-processing.

```
python scripts/build_dataset.py --data_dir ../data \
    --dataset sst --split train --arch google/bigbird-roberta-base 

python scripts/build_dataset.py --data_dir ../data \
    --dataset sst --split dev --arch google/bigbird-roberta-base 

python scripts/build_dataset.py --data_dir ../data \
    --dataset sst --split test --arch google/bigbird-roberta-base 

```

If the dataset is very large, you have the option to subsample part of the dataset for smaller-scale experiements. For example, in the command below, we build a train set with only 1000 train examples (sampled with seed 0).
```
python scripts/build_dataset.py \
    --data_dir ../data \
    --dataset sst \
    --split train \
    --arch google/bigbird-roberta-base \
    --num_samples 1000 \
    --seed 0
```

By default, for explanation regularization, we provide gold rationales for all train instances. However, in practical settings, there is often a budget of how many gold rationales we can annotate. To simulate this, after building the dataset (using the previous commands), we can select a subset of train instances to provide gold rationales for. To select this subset, we specify the selection strategy (`train_rationale_selection`), percentage of train instances with gold rationales (`pct_train_rationales`), and seed for sampling train instances (`seed`). Note that `seed` is only needed if `train_rationale_selection` is a random process (e.g., `uniform`).
```
python scripts/build_dataset.py \
    --data_dir ../data \
    --dataset sst \
    --split train \
    --arch google/bigbird-roberta-base \
    --train_rationale_selection uniform \
    --pct_train_rationales 10.0 \
    --seed 0
```

## 2. Train Task LM

The command below is the most basic way to run `main.py` and will train the Task LM without any explanation regularization (`model=lm`). 

However, since all models need to be evaluated w.r.t. explainability metrics, we need to specify an attribution algorithm for computing post-hoc explanations. This is done by setting `model.explainer_type=attr_algo` to specify that we are using an attribution algorithm based explainer (as opposed to `lm` or `self_lm`), `model.attr_algo` to specify the attribution algorithm, and `model.attr_pooling` to specify the attribution pooler.
```
python main.py -m \
    data=sst \
    model=lm \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=32 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=32 \
    setup.eval_batch_size=32 \
    setup.num_workers=3 \
    seed=0,1,2
```

By default, checkpoints will not be saved (i.e., `save_checkpoint=False`), so you need to set `save_checkpoint=True` if you want to save the best checkpoint.
```
python main.py -m \
    save_checkpoint=True \
    data=sst \
    model=lm \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=32 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=32 \
    setup.eval_batch_size=32 \
    setup.num_workers=3 \
    seed=0,1,2
```

## 3. Train Task LM with Explanation Regularization (ER)
We can also train the Task LM with ER (`model=expl_reg`). ER can be done using pre-annotated gold rationales or human-in-the-loop feedback.

### **Task LM + ER (all gold rationales)**
Provide gold rationales for all train instances:
```
python main.py -m \
    save_checkpoint=True \
    data=sst \
    model=expl_reg \
    model.attr_algo=input-x-gradient \
    model.task_wt=1.0 \
    model.pos_expl_wt=0.5 \
    model.pos_expl_criterion=bce \
    model.neg_expl_wt=0.5 \
    model.neg_expl_criterion=l1 \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=32 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=32 \
    setup.eval_batch_size=32 \
    setup.num_workers=3 \
    seed=0,1,2
```

### **Task LM + ER (10% gold rationales; uniform)**
Provide gold rationales for 10% of train instances, which are sampled uniformly:
```
python main.py -m \
    save_checkpoint=True \
    data=sst \
    data.pct_train_rationales=10.0 \
    data.pct_train_rationales_seed=0,1,2 \
    data.train_rationale_selection=uniform \
    model=expl_reg \
    model.attr_algo=input-x-gradient \
    model.task_wt=1.0 \
    model.pos_expl_wt=0.5 \
    model.pos_expl_criterion=bce \
    model.neg_expl_wt=0.5 \
    model.neg_expl_criterion=l1 \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=32 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=32 \
    setup.eval_batch_size=32 \
    setup.num_workers=3 \
    seed=0,1,2
```
