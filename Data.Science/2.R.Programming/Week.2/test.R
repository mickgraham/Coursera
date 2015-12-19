## Matrix inversion is usually a costly computation and their may be some benefit to caching the inverse of a 
## matrix rather than compute it repeatedly 

## Code described below, shows a pair of functions that cache the inverse of a matrix.



## Function "makeCacheMAtrix" creates a special "matrix" object that can cache its inverse.
## It contains all the objects (functions) needed to run the operations: set, get, setInverse and getInverse
## It makes possible to save data in cache in order to run faster


makeCacheMatrix2 <- function(x = matrix()) { # input x will be a matrix
        m <- NULL #  m will store our INVERSE and it's reset to NULL every 
        #    time makeCacheMAtrix is called
        
        set <- function(y) {  #this function set values for a matrix. It is neccesary to run cacheSolve
                x <<- y         # saves matrix in var x. Be careful, x is saved in other environment  
                m <<- NULL      # reset our INVERSE every time function set is called
        }
        
        get <- function() x    # Returns the value of the original vector
        
        setInverse <- function(matrix) m <<- matrix # cacheSolve() will call setInverse in the first
        #  call and it will store the value using superassignment 
        
        getInverse <- function() m # this will return the cached value on subsequent accesses
        # this is only to show you that the mean has been stored and does not affect anything
        
        list(set = set, get = get,
             setInverse = setInverse,
             getInverse = getInverse)
        # This list saves the functions created above. When an new object is created
        # returns all functions in the list. If the function is not in the list
        # it cannot be accessed 
}



## This function, "cacheSolve" computes the inverse of the special "matrix" returned by makeCacheMatrix above. 
## If the inverse has already been calculated (and the matrix has not changed), 
## then the cachesolve should retrieve the inverse from the cache.

## Return a matrix that is the inverse of 'x'
cacheSolve2 <- function(x, ...) { # the input is an object created by makeCacheMatrix
        m <- x$getInverse()     # checks to see if the Inverse has already been calculated
        
        if(!is.null(m)) {                  # if Inverse has already been calculated, enter and...
                message("getting cached data")   #...shows a message in the console and....
                return(m)                        #...returns the Inverse
        }
        
        # if the inverse has not already been calculated...enter here
        data <- x$get()         # we save our original Matrix in a variable 
        m <- solve(data)        # calculates the Inverse of our matrix and save in "m"
        x$setInverse(m)         # store the calculated Inverse in x (see setInverse() in makeCacheMatrix)
        m                       # Finally return the Inverse to the code that called this function
}        