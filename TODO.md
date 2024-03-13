# TODO list for this project.


- 1. Write form and view to add new poll
- 2. Add functionality to search for poll

- 3. Add functionality to vote on polls
- 4. Write user profile views and template
- 5. Add author attribute to Question class
- 6. Add voters attribute to Choice class




## ISSUES
1. 
    
    
## ADDED
1. Added `unfollow` to the action type in the notification models
2. Added the `unfollow` option to correctly formar the appropriate notification type in the notification page


`<link rel="stylesheet" href="{% static 'css/script.css' %}">`
`<script src="{% static 'js/script.js' %}">   </script>`




/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./journal/**/*.{html,js}",
    "./accounts/**/*.{html,js}"            
],
  theme: {
    extend: {
      colors: {
        "mindcream": "#FFFFDB",
        "mindpurple": "#700170",
        "mindtextmetal": "#121212"

      }
    },
  },
  plugins: [],
}

