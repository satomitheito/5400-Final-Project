import logging


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        filename="../../../logs.txt",
        filemode='w',
        format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
        )
    
    logger = logging.getLogger(__name__)  # Main module logger
    logger.info("Starting main program")