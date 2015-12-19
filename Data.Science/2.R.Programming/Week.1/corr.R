corr <- function(directory, threshold = 0) {
        ## 'directory' is a character vector of length 1 indicating
        ## the location of the CSV files
        
        ## 'threshold' is a numeric vector of length 1 indicating the
        ## number of completely observed observations (on all
        ## variables) required to compute the correlation between
        ## nitrate and sulfate; the default is 0
        
        ## Return a numeric vector of correlations
        
        # Create a list of files.
        files_list <- list.files(directory, full.names=TRUE)
        
        # Create an empty data frame.
        dat <- numeric()
        
        # Loop through the files, rbinding them together.
        for (i in seq_along(files_list)) {
                
                # Get the number of completely observed cases.
                complete_dat <- complete(directory, i)
                
                # Check the threshold.
                if (complete_dat[1, "nobs"] > threshold) {

                        # Extract the file data.
                        csv_dat <- read.csv(files_list[i])
                        csv_dat <- csv_dat[complete.cases(csv_dat[,2:3]), ]
                        sulfate_dat <- csv_dat[, "sulfate"]
                        nitrate_dat <- csv_dat[, "nitrate"]
                        
                        # Calculate the correlation between sulfate and nitrate.
                        cor_dat <- cor(sulfate_dat, nitrate_dat)
                        
                        # Add the correlation.
                        dat <- c(dat, cor_dat)
                }
        }
        
        # Return the vector of correlations.
        dat
}