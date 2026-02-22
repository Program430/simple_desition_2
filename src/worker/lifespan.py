from structlog.contextvars import bind_contextvars, clear_contextvars
from celery.signals import worker_process_init, worker_process_shutdown, task_prerun, task_postrun

from src.share.core.logger import get_logger, setup_logger
from src.worker.utiles.async_loop_manager import manager


logger = get_logger()


@worker_process_init.connect
def setup_tasks(sender, **kwargs):
    setup_logger()
    manager.start()
    
    
@worker_process_shutdown.connect
def shutdown_tasks(sender, **kwargs):
    manager.stop()
    

@task_prerun.connect
def setup_task_context(task_id, task, args, kwargs, **others):
    bind_contextvars(task_id=task_id)


@task_postrun.connect
def cleanup_task_context(task_id, task, **kwargs):
    clear_contextvars()
