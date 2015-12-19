pollutantmean <- function(directory, pollutant, id = 1:332) {
        ## 'directory' is a character vector of length 1 indicating
        #A# the location of the CSV files

        ## 'pollutant' is a character vector of length 1 indicating
        ## the name of the pollutant for which we will calculate the
        ## mean; either "sulfate" or "nitrate".
        
        ## 'id' is an integer vector indicating the monitor ID numbers
        ## to be used

        ## Return the mean of the pollutant across all monitors list
        ## in the 'id' vector (ignoring NA values)
        
        # Create a list of files.
        files_list <- list.files(directory, full.names=TRUE)
        
        # Create an empty data frame.
        dat <- data.frame()
        
        # Loop through the files, rbinding them together.
        for (i in id) {
                dat <- rbind(dat, read.csv(files_list[i]))
        }
        
        # Subset of the ‘pollutant’ column of the data where 'ID' in 'id'.
        dat_subset <- dat[which(dat[, "ID"] %in% id), pollutant]
        
        # Calculate the mean.
        mean(dat_subset, na.rm=TRUE)
}