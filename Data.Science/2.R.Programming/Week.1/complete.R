complete <- function(directory, id = 1:332) {
        ## 'directory' is a character vector of length 1 indicating
        ## the location of the CSV files
        
        ## 'id' is an integer vector indicating the monitor ID numbers
        ## to be used
        
        ## Return a data frame of the form:
        ## id nobs
        ## 1  117
        ## 2  1041
        ## ...
        ## where 'id' is the monitor ID number and 'nobs' is the
        ## number of complete cases
        
        # Create a list of files.
        files_list <- list.files(directory, full.names=TRUE)
        
        # Create an empty data frame.
        dat <- data.frame()
        
        # Loop through the files, rbinding them together.
        for (i in id) {
                # Extract the file data.
                id <- i
                nobs <- sum(complete.cases(read.csv(files_list[i])))
                id_nobs <- c(id, nobs)
                
                # Add the file data to the data frame.
                dat <- rbind(dat, id_nobs)
        }
        
        # Name the columns.
        col_headings <- c('id','nobs')
        names(dat) <- col_headings
        
        # Display the data frame.
        dat
}