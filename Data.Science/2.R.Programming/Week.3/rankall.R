## For each state, find the hospital of the given rank.
## Return a data frame with the hospital names and the (abbreviated) state name.
rankall <- function(outcome, num = "best") {
        
        ## Read outcome data.
        data <- read.csv("data/outcome-of-care-measures.csv",
                         colClasses = "character")

        ## Check that outcome is valid.
        o <- NULL
        if (outcome == "heart attack") {
                o <- "Hospital.30.Day.Death..Mortality..Rates.from.Heart.Attack"
        }
        else if (outcome == "heart failure") {
                o<-"Hospital.30.Day.Death..Mortality..Rates.from.Heart.Failure"
        }
        else if (outcome == "pneumonia") {
                o <- "Hospital.30.Day.Death..Mortality..Rates.from.Pneumonia"
        }
        else {
                stop("invalid outcome")
        }
        
        # Assign values to the best and worst rankings.
        d <- FALSE
        if (num == "best") {
                num <- 1
        }
        else if (num == "worst") {
                num <- 1
                d <- TRUE
        }
        
        # Get the unique states.
        data_states <- sort(unique(data[, "State"]))
        
        # Create an empty data frame.
        dat <- data.frame()
        
        # Add a record for each state.
        for (s in data_states) {
                
                # Only include records for the supplied state.
                data_subset <- data[which(data[, "State"] %in% s), ]
                
                # Make the outcome column values numeric.
                data_subset[, o] <-
                        suppressWarnings(as.numeric(data_subset[, o]))
                
                # Sort the data using an ordered vector.
                data_ordered <- order(data_subset[, o],
                                      data_subset[, "Hospital.Name"],
                                      na.last = TRUE,
                                      decreasing = d)
                data_sorted <- data_subset[data_ordered, ]
                
                # Get the hospital name of the record with the specified rank.
                if (num <= nrow(data_sorted)) {
                        name <- as.character(data_sorted[num, "Hospital.Name"])
                }
                else {
                        name <- NA
                }
                dat <- rbind(dat, data.frame(name, s))
        }
        
        # Name the rows and columns.
        colnames(dat) <- c("hospital", "state")
        rownames(dat) <- dat[, "state"]

        # Return the data frame.
        dat
}