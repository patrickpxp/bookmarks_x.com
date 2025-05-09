import random
import os
from playwright.sync_api import sync_playwright, Page, Locator
from datetime import datetime
import json
import urllib.parse

def post_saved(post_id): # TODO : make this generic, not just for files, should work for databases or any
     if os.path.isfile(post_id+".json"): 
          return True

def save_post(post_id, post_contents): # TODO : make this generic, not just for files, should work for databases or any
    filename = f"{post_id }.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({'id':post_id, 'content': post_contents}, f, indent=4)

def get_bookmarks(page: Page):
    scroll_height = page.evaluate("document.body.scrollHeight")
    
    posts = page.locator("article")
    
    for post in posts.all():
        post_path = post.locator("a:has(time)").get_attribute("href") # '/rohanpaul_ai/status/1920069397277774228'
        post_id = post_path.replace("/status/","$").replace("/","") #'rohanpaul_ai$1920069397277774228' # I think $ is not allowed in usernames so it's a good separator
        post_contents = post.inner_html()
        if post_saved(post_id):
                print("post already saved : ",post_id)
                continue
        else:
            save_post(post_id,post_contents)
            print("saved post ", post_id)

def main():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)

    state_file = "state.json"

    if not os.path.isfile(state_file): # check if state file present
        print("no state file present, let's login")
        context = browser.new_context()
        page = context.new_page()
        page.goto('https://x.com/i/bookmarks')
        page.wait_for_selector("button[aria-label='Account menu']", state="attached", timeout=30000) # wait for login to appear
        context.storage_state(path="state.json")
        page.wait_for_timeout(random.randint(1000,5000)) # wait to look human
    else: # there is a state file present
        context = browser.new_context(storage_state=state_file)
        page = context.new_page()
        page.goto('https://x.com/i/bookmarks')
        page.wait_for_timeout(random.randint(1000,5000)) # wait to look human
        # now, check we actually are logged in
        if page.locator("button[aria-label='Account menu']").count()  != 1 :
             raise Exception("Looks like the provided state file is not logged in to X.com (or couldn't detect login state in browser). Delete the state file and run the script again")
    get_bookmarks(page)
    # close everything
    browser.close()
    playwright.stop()

if __name__ == "__main__":
    main()