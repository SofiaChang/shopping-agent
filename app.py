import streamlit as st
from agent.shopping_agent import ShoppingAgent
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    if "agent" not in st.session_state:
        st.session_state.agent = ShoppingAgent(enable_history=True)
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "new_search" not in st.session_state:
        st.session_state.new_search = False
    
    st.title("🛍️ Personal Shopping Agent")
    st.write("Enter your shopping request below.")
    
    if st.button("New Search"):
        st.session_state.new_search = True
    
    if st.session_state.new_search:
        st.session_state.conversation_history = []
        st.session_state.agent.close()
        st.session_state.agent = ShoppingAgent(enable_history=True)
        st.session_state.new_search = False
    
    user_input = st.text_input(
        "What would you like to search for?", 
        placeholder="e.g., 'Find me a laptop under $1000 with excellent ratings'"
    )
    
    search_button = st.button("Search")
    
    if search_button and user_input:
        with st.spinner("Searching for products..."):
            try:
                results = st.session_state.agent.handle_request(user_input)
                
                agent_summary = f"Found {len(results['products'])} main matches"
                if results['other_products']:
                    agent_summary += f", plus {len(results['other_products'])} other suggestions"
                agent_summary += "."
                
                st.session_state.conversation_history.append({
                    "input": user_input,
                    "results": len(results["products"]) + len(results["other_products"])
                })
                
                if results["products"]:
                    st.header("Top Results")
                    st.write(f"Found {len(results['products'])} products that match all your criteria:")
                    for product in results["products"]:
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            if product.get("thumbnail"):
                                st.image(product["thumbnail"], use_container_width=True)
                        
                        with col2:
                            if product.get("url"):
                                st.markdown(f"[**{product['title']}**]({product['url']})")
                            else:
                                st.subheader(product["title"])
                            
                            st.write(f"Price: ${product['price']:.2f}")
                            st.write(f"Rating: {product['rating']} ⭐")
                            st.write(f"Reviews: {product['review_count']:,}")
                            prime_status = "✅" if product.get('prime') else "❌"
                            st.write(f"Prime: {prime_status}")
                        
                        st.markdown("---")
                
                if results["other_products"]:
                    st.header("Other Suggestions")
                    st.write(f"Found {len(results['other_products'])} additional products that might interest you:")
                    for product in results["other_products"]:
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            if product.get("thumbnail"):
                                st.image(product["thumbnail"], use_container_width=True)
                        
                        with col2:
                            if product.get("url"):
                                st.markdown(f"[**{product['title']}**]({product['url']})")
                            else:
                                st.subheader(product["title"])
                            
                            st.write(f"Price: ${product['price']:.2f}" if product['price'] is not None else "Price: Not available")
                            st.write(f"Rating: {product['rating']} ⭐" if product['rating'] is not None else "Rating: Not available")
                            st.write(f"Reviews: {product['review_count']:,}") if product['review_count'] is not None else "Reviews: Not available"
                            prime_status = "✅" if product.get('prime') else "❌"
                            st.write(f"Prime: {prime_status}")

                            if 'filter_reasons' in product:
                                st.write("Didn't fully meet constraints:")
                                for reason in product['filter_reasons']:
                                    st.write(f"- {reason}")
                        
                        st.markdown("---")
                
                if not results["products"] and not results["other_products"]:
                    st.warning("No products found matching your criteria. Try adjusting your search.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error in main: {str(e)}", exc_info=True)
    
    if st.session_state.conversation_history:
        st.header("Conversation History")
        for entry in reversed(st.session_state.conversation_history):
            st.write(f"- {entry['input']}: {entry['results']} results")

if __name__ == "__main__":
    main()
