import pytorch_lightning as pl
from pytorch_lightning.callbacks import Callback

class BestPerformance(Callback):

    def __init__(self, monitor, mode):
        super().__init__()

        self.monitor = monitor
        assert monitor.split('_')[0] == 'dev'
        self.test_monitor = '_'.join(['test'] + monitor.split('_')[1:])

        self.mode = mode
        assert mode in ['max', 'min']

    def on_validation_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        if self.mode == 'max':
            if pl_module.best_metrics['dev_best_perf'] == None:
                assert pl_module.best_metrics['test_best_perf'] == None
                pl_module.best_metrics['dev_best_perf'] = -float('inf')

            if trainer.callback_metrics[self.monitor] > pl_module.best_metrics['dev_best_perf']:
                pl_module.best_metrics['dev_best_loss'] = trainer.callback_metrics['dev_loss_epoch']
                pl_module.best_metrics['dev_best_perf'] = trainer.callback_metrics[self.monitor]
                pl_module.best_metrics['test_best_perf'] = trainer.callback_metrics[self.test_monitor]
                pl_module.best_metrics['best_epoch'] = trainer.current_epoch

        else:
            if pl_module.best_metrics['dev_best_loss'] == None:
                assert pl_module.best_metrics['test_best_perf'] == None
                pl_module.best_metrics['dev_best_loss'] = float('inf')

            if trainer.callback_metrics[self.monitor] < pl_module.best_metrics['dev_best_loss']:
                pl_module.best_metrics['dev_best_loss'] = trainer.callback_metrics[self.monitor]
                pl_module.best_metrics['dev_best_perf'] = trainer.callback_metrics['dev_acc_metric_epoch']
                pl_module.best_metrics['test_best_perf'] = trainer.callback_metrics['test_acc_metric_epoch']
                pl_module.best_metrics['best_epoch'] = trainer.current_epoch

        pl_module.log('dev_best_perf', pl_module.best_metrics['dev_best_perf'], prog_bar=True, sync_dist=True)
        pl_module.log('test_best_perf', pl_module.best_metrics['test_best_perf'], prog_bar=True, sync_dist=True)
        pl_module.log('best_epoch', pl_module.best_metrics['best_epoch'], prog_bar=True, sync_dist=True)