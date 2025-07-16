# Post APIs

  Method      	   URL	             Purpose
- GET	          /api/posts/	     Get list of all - posts
- POST	          /api/posts/	     Create a new post (authenticated only)
- GET	          /api/posts/{id}/   Get details of a single post
- PUT or PATCH    /api/posts/{id}/	 Update a post (owner only)
- DELETE	      /api/posts/{id}/	 Delete a post (owner only)

#  Like/Dislike Actions

  Method	  URL	                     What it does
- POST	     /api/posts/{id}/like/	     Like the post (only once)
- POST	     /api/posts/{id}/dislike/	 Dislike the post (only once)

# Search Posts

Method	       URL	                                             
- GET	       /api/posts/?search={title or description}  

# Comment APIs

  Method	    URL	                            Purpose
- GET	        /api/comments/	                Get list of all top-level comments
- GET	        /api/comments/?post={post_id}	Get top-level comments for a specific post
- POST	        /api/comments/	                Add a new comment or reply
- GET	        /api/comments/{id}/	            Get a single comment
- PUT or PATCH	/api/comments/{id}/	            Update a comment (owner only)
- DELETE        /api/comments/{id}/	            Delete a comment (owner only)


