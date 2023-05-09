# TODO list for this project.


- 1. Write form and view to add new poll
2. Add functionality to search for poll

- 3. Add functionality to vote on polls
- 4. Write user profile views and template
- 5. Add author attribute to Question class
- 6. Add voters attribute to Choice class




## ISSUES
1. Redirect users back to the last page(profile page or homepage) after deleting a poll
2. Show a message reads "Only poll authors can delete polls" when users try to delete a poll they didn't create
3. Fix the ***MultiValueDictKeyError at /vote/: 'option_pk'*** error on hitting `vote` without choosing an option.
4. Users should be able to go to their profile page directly from anywhere in the app. At the moment, users  won't be taken to their page on clicking on the profile button from another user's profile page but will remain in the that user's page. 
5. Clicking the `like` button adds the user to the liker. I used `{{ question.likers|length }}` but the number of (likers)likes is not reflecting on the poll.  



## ADDED
1. Created a comment model to represent poll comments
2. Updated Question model to implement 'likes'
3. Updated the details page to show comments and number of likes 
4. Users can now add comments under polls
