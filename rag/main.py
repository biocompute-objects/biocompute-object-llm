from bcorag import misc_functions as misc_fns
from bcorag import option_picker as op
from bcorag.bcorag import BcoRag

def main():

    logger = misc_fns.setup_root_logger("./logs/bcorag.log")
    logger.info('################################## RUN START ##################################')
    
    # get the user choices
    user_choices = op.initialize_picker()
    if user_choices is None:
        misc_fns.graceful_exit()

    # handle domain generation
    bco_rag = BcoRag(user_choices) # type: ignore
    while True:
        domain = bco_rag.choose_domain()
        if domain is None:
            misc_fns.graceful_exit()
        _ = bco_rag.perform_query(domain) # type: ignore
        print(f"Successfully generated the {domain} domain.\n")

if __name__ == "__main__":
    main()
