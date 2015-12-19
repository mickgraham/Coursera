## These functions cache the inverse of a matrix.

## Matrix inversion is usually a costly computation and their may be some
## benefit to caching the inverse of a matrix rather than compute it repeatedly.

## This function creates a special "matrix" object that can cache its inverse.
makeCacheMatrix <- function(x = matrix()) {
        
        # Reset the stored inverse to NULL when makeCacheMatrix is called.
        i <- NULL
        
        # Function that stores the matrix and resets the inverse.
        set <- function(y) {
                x <<- y
                i <<- NULL
        }
        
        # function that gets the stored matrix.
        get <- function() {
                x
        }
        
        # Function that stores the inverse of the stored matrix.
        setinverse <- function(inverse) {
                i <<- inverse
        }
        
        # Function that gets the inverse of the stored matrix.
        getinverse <- function() {
                i
        }
        
        # Return the list of functions that are part of the object.
        list(set = set,
             get = get,
             setinverse = setinverse,
             getinverse = getinverse)
}


## This function computes the inverse of the special "matrix" returned by the
## makeCacheMatrix function.
cacheSolve <- function(x, ...) {
        
        # Get the stored inverse from 'x'.
        i <- x$getinverse()
        
        # Return the stored inverse if it is not NULL.
        if(!is.null(i)) {
                message("getting cached data")
                return(i)
        }
        
        # Get the stored matrix in 'x', compute the inverse, and store in 'x'.
        data <- x$get()
        i <- solve(data, ...)
        x$setinverse(i)
        
        # Return the computed inverse.
        i
}