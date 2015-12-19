## Finds the hospital name in a state with given rank 30-day death rate outcome.
rankhospital <- function(state, outcome, num = "best") {
        
        ## Read outcome data.
        data <- read.csv("data/outcome-of-care-measures.csv",
                         colClasses = "character")
        
        ## Check that state is valid.
        s <- NULL
        if (state %in% data[, "State"]) {
                s <- state
        }
        else {
                stop("invalid state")
        }
        
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
        
        # Only include records for the supplied state.
        data_subset <- data[which(data[, "State"] %in% s), ]
        
        # Make the outcome column values numeric.
        data_subset[, o] <- suppressWarnings(as.numeric(data_subset[, o]))
        
        # Assign values to the best and worst rankings.
        d <- FALSE
        if (num == "best") {
                num = 1
        }
        else if (num == "worst") {
                num = 1
                d <- TRUE
        }
        
        # Sort the data using an ordered vector.
        data_ordered <- order(data_subset[, o],
                              data_subset[, "Hospital.Name"],
                              na.last = TRUE,
                              decreasing = d)
        data_sorted <- data_subset[data_ordered, ]

        # Return the hospital name of the record with the specified rank.
        if (num <= nrow(data_sorted)) {
                data_sorted[num, "Hospital.Name"]
        }
        else {
                NA
        }
}

context("rankhospital")

test_that("outcome testing works", {
        expect_that(rankhospital("TX", "heart failure", 4),
                    equals("DETAR HOSPITAL NAVARRO"))
        expect_that(rankhospital("MD", "heart attack", "worst"),
                    equals("HARFORD MEMORIAL HOSPITAL"))
        expect_that(rankhospital("MN", "heart attack", 5000),
                    equals(NA))
})