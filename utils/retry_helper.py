import time
import functools

def retry(max_attempts=3, delay=2, backoff=2, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    print(f"[yellow]Retry {attempts}/{max_attempts} after error: {e}[/yellow]")
                    time.sleep(current_delay)
                    current_delay *= backoff
            raise Exception(f"[red]All {max_attempts} retry attempts failed for {func.__name__}[/red]")
        return wrapper
    return decorator
