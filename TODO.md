# TODO list for this project.


- 1. Write form and view to add new poll
2. Add functionality to search for poll

- 3. Add functionality to vote on polls
- 4. Write user profile views and template
- 5. Add author attribute to Question class
- 6. Add voters attribute to Choice class




## ISSUES
1. 
2. 
3. Fix the ***MultiValueDictKeyError at /vote/: 'option_pk'*** error on hitting `vote` without choosing an option.
4. Users should be able to go to their profile page directly from anywhere in the app. At the moment, users  won't be taken to their page on clicking on the profile button from another user's profile page but will remain in the that user's page.   

5. Add Display name to the UserProfile model to display on profile page



## ADDED
1. Fixed issue ***No.4*** by passing `request.user` to the profile route instead of just `user` which might cause conflict
when the authenticated user is on another user's page 
2. Fixed issue ***No.3*** by try catching any error that might occur while getting `request.POST['option.pk']` and redirecting to the previous page with `request.META.get('HTTP_REFERER', reverse('poll:home'))` 