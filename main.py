import logging
from agent.shopping_agent import ShoppingAgent


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    agent = ShoppingAgent(enable_history=True)
    
    print("\nWelcome to the Shopping Agent!")
    print("You can:")
    print("- Enter a shopping request (e.g., 'Find me a coffee maker under $100')")
    print("- Refine your search with partial queries (e.g., 'with Prime shipping')")
    print("- Type 'new' to start a fresh search")
    print("- Type 'quit' to exit")
    print("- Type 'history' to see your search history")
    
    try:
        while True:
            user_input = input("\nEnter your shopping request or partial refinement: ").strip()
            
            if user_input.lower() == 'quit':
                print("\nExiting...")
                break
                
            if user_input.lower() == 'new':
                agent = ShoppingAgent(enable_history=True)
                print("\nStarting a new search session.")
                continue
                
            if user_input.lower() == 'history':
                if agent.history:
                    print("\nSearch History:")
                    for entry in agent.history:
                        print(f"- {entry['input']}: {entry['results']} results")
                else:
                    print("\nNo search history available.")
                continue
            
            try:
                results = agent.handle_request(user_input)
                
                if results["products"]:
                    print(f"\nFound {len(results['products'])} products matching your criteria:")
                    for i, product in enumerate(results["products"], 1):
                        print(f"\nProduct {i}:")
                        print(f"Title: {product.get('title', 'Unknown Product')}")
                        print(f"Price: ${product.get('price', 'N/A'):.2f}")
                        print(f"Rating: {product.get('rating', 'N/A'):.1f} ⭐")
                        print(f"Reviews: {product.get('review_count', 'N/A'):,}")
                        print(f"Prime: {'✅' if product.get('prime', False) else '❌'}")
                
                if results["other_products"]:
                    print(f"\nFound {len(results['other_products'])} additional suggestions:")
                    for i, product in enumerate(results["other_products"], 1):
                        print(f"\nSuggestion {i}:")
                        print(f"Title: {product.get('title', 'Unknown Product')}")
                        print(f"Price: ${product.get('price', 'N/A'):.2f}")
                        if 'filter_reasons' in product:
                            print("Didn't fully meet constraints:")
                            for reason in product['filter_reasons']:
                                print(f"- {reason}")
                
                if not results["products"] and not results["other_products"]:
                    print("\nNo products found matching your criteria. Try adjusting your search.")
            
            except Exception as e:
                print(f"\nError processing request: {str(e)}")
                logger.error(f"Error processing request: {str(e)}", exc_info=True)
    
    except KeyboardInterrupt:
        print("\n\nSearch cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        logger.error(f"Error in main: {str(e)}", exc_info=True)
    finally:
        agent.close()

if __name__ == "__main__":
    main()