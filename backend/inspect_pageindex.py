try:
    import pageindex
    print("PageIndex package found.")
    print(dir(pageindex))
    if hasattr(pageindex, 'PageIndexClient'):
        from pageindex import PageIndexClient
        print("PageIndexClient attributes:")
        # We can't init without API key maybe, so just print dir of class
        print(dir(PageIndexClient))
except ImportError:
    print("PageIndex package NOT found.")
except Exception as e:
    print(f"Error: {e}")
