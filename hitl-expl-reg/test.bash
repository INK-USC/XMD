python scripts/build_dataset.py --data_dir data \
    --dataset hatexplain --split train --arch google/bigbird-roberta-base

python scripts/build_dataset.py --data_dir ../data \
    --dataset sst --split dev --arch google/bigbird-roberta-base

python scripts/build_dataset.py --data_dir ../data \
    --dataset sst --split test --arch google/bigbird-roberta-base

CUDA_VISIBLE_DEVICES=1 python main.py -m \
    save_checkpoint=True \
    data=hatexplain \
    model=lm \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=16 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=16 \
    setup.eval_batch_size=16 \
    setup.num_workers=3 \
    seed=0 \
    logger.name=hatexplain


CUDA_VISIBLE_DEVICES=2 python main.py -m \
    save_checkpoint=True \
    data=sst \
    model=lm \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=32 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=32 \
    setup.eval_batch_size=32 \
    setup.num_workers=3 \
    seed=0 \
    logger.name=sst


CUDA_VISIBLE_DEVICES=2 python main.py -m \
    save_checkpoint=True \
    data=sst \
    model=lm \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=32 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=32 \
    setup.eval_batch_size=32 \
    setup.num_workers=3 \
    seed=0 \
    logger.name=sst

python main.py \
    training.ckpt_path=save/lm_sst_google/bigbird-roberta-base_01_06_2022_44081e0f/checkpoints/best.ckpt

python main.py \
  training=evaluate \
  data.dataset=sst \
  training.ckpt_path=lm_sst_google/bigbird-roberta-base_01_06_2022_44081e0f/checkpoints/best.ckpt \
  training.eval_splits=\'train,dev,test\'

CUDA_VISIBLE_DEVICES=1 python main.py \
  training=evaluate \
  data.dataset=sst \
  training.ckpt_path=lm_sst_google/full_reg_add_mae/checkpoints/best.ckpt \
  training.eval_splits=\'test\'

CUDA_VISIBLE_DEVICES=0 python main.py \
  training=evaluate \
  data.dataset=amazon \
  training.ckpt_path=lm_sst_google/full_reg_add_mae/checkpoints/best.ckpt \
  training.eval_splits=\'test\'

CUDA_VISIBLE_DEVICES=2 python main.py \
training=evaluate \
data.dataset=yelp \
training.ckpt_path=lm_sst_google/full_reg_add_mae/checkpoints/best.ckpt \
training.eval_splits=\'test\'

CUDA_VISIBLE_DEVICES=2 python main.py \
  training=evaluate \
  data.dataset=amazon \
  training.ckpt_path=lm_sst_google/full_reg_add_mse/checkpoints/best.ckpt \
  training.eval_splits=\'test\'

CUDA_VISIBLE_DEVICES=2 python main.py \
  training=evaluate \
  data.dataset=yelp \
  training.ckpt_path=lm_sst_google/full_reg_add_mse/checkpoints/best.ckpt \
  training.eval_splits=\'test\'

CUDA_VISIBLE_DEVICES=2 python main.py -m \
    save_checkpoint=True \
    data=sst \
    model=lm \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=32 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=32 \
    setup.eval_batch_size=32 \
    setup.num_workers=3 \
    seed=0,1,2 \
    logger.name=test2 \

CUDA_VISIBLE_DEVICES=2 python main.py -m \
    save_checkpoint=True \
    data=sst \
    model=expl_reg \
    model.attr_algo=input-x-gradient \
    model.task_wt=1.0 \
    model.pos_expl_wt=1 \
    model.pos_expl_criterion=l1 \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=32 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=32 \
    setup.eval_batch_size=32 \
    setup.num_workers=3 \
    seed=0


CUDA_VISIBLE_DEVICES=0 python main.py -m \
    save_checkpoint=True \
    data=hatexplain \
    model=expl_reg \
    model.attr_algo=input-x-gradient \
    model.task_wt=1.0 \
    model.pos_expl_wt=1 \
    model.pos_expl_criterion=l1 \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=8 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=8 \
    setup.eval_batch_size=8 \
    setup.num_workers=3 \
    seed=0

CUDA_VISIBLE_DEVICES=1 python main.py -m \
    save_checkpoint=True \
    data=hatexplain \
    model=lm \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=8 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=8 \
    setup.eval_batch_size=8 \
    setup.num_workers=3 \
    seed=0

CUDA_VISIBLE_DEVICES=2 python main.py -m \
    save_checkpoint=True \
    data=hatexplain \
    model=expl_reg \
    model.attr_algo=input-x-gradient \
    model.task_wt=1.0 \
    model.pos_expl_wt=1 \
    model.pos_expl_criterion=l1 \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=8 \
    setup.accumulate_grad_batches=1 \
    setup.eff_train_batch_size=8 \
    setup.eval_batch_size=8 \
    setup.num_workers=3 \
    seed=0

CUDA_VISIBLE_DEVICES=0 python main.py -m \
    save_checkpoint=True \
    data=hatexplain \
    model=expl_reg \
    model.attr_algo=input-x-gradient \
    model.task_wt=1.0 \
    model.pos_expl_wt=1 \
    model.pos_expl_criterion=mse \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=8 \
    setup.accumulate_grad_batches=2 \
    setup.eff_train_batch_size=16 \
    setup.eval_batch_size=16 \
    setup.num_workers=3 \
    seed=0

CUDA_VISIBLE_DEVICES=2 python main.py -m \
    save_checkpoint=True \
    data=sst \
    model=expl_reg \
    model.attr_algo=input-x-gradient \
    model.task_wt=1.0 \
    model.pos_expl_wt=1 \
    model.pos_expl_criterion=l1 \
    model.optimizer.lr=2e-5 \
    setup.train_batch_size=8 \
    setup.accumulate_grad_batches=2 \
    setup.eff_train_batch_size=16 \
    setup.eval_batch_size=16 \
    setup.num_workers=3 \
    seed=0