# TODO list for this project.


- 1. Write form and view to add new poll
- 2. Add functionality to search for poll

- 3. Add functionality to vote on polls
- 4. Write user profile views and template
- 5. Add author attribute to Question class
- 6. Add voters attribute to Choice class




## ISSUES
1. In an attempt to properly implement the notification page, I encountered errors which do not seem consistent making it difficult to pinpoint the cause. Namely;
    - A situation where not all of the user's notifications is properly formatted according to the templates in `notifications.html`

    - `Reverse for 'profile' with arguments '('',)' not found. 1 pattern(s) tried: ['users/(?P<username>[^/]+)$']` 
    I think its getting a user without an id(`pk`) which is not supposed to happen considering all users should have an *id* as the `pk`.
    Note: This error isn't raised all the time so i think the problem is with the user objects ive created and not the templates or view files
    
    



## ADDED
1. 


