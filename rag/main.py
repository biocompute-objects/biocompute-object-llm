from bcorag import pipeline
from bcorag import misc_functions as misc_fns

def main():

    logger = misc_fns.setup_root_logger("./logs/bcorag.log")
    logger.info('################################## RUN Start ##################################')
    
    # get the user choices
    user_picks = pipeline.initalize_step()
    if user_picks is None:
        misc_fns.graceful_exit()
    for option, selection in user_picks.items():
        logger.info("User selections:")
        logger.info(f"\t{option}: {selection}")

    # handle domain generation
    bco_rag = pipeline.retrieve_bco_rag(user_picks)
    print(bco_rag.perform_query("usability"))

if __name__ == "__main__":
    main()
