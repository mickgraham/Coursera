## Finds the hospital name in a state with lowest 30-day death rate outcome.
best <- function(state, outcome) {
        
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

        # Sort the data using an ordered vector.
        data_ordered <- order(data_subset[, o], data_subset[, "Hospital.Name"])
        data_sorted <- data_subset[data_ordered, ]
        
        # Return the hospital name of the first record.
        data_sorted[1, "Hospital.Name"]
}

context("best")

test_that("best function computation works", {
        expect_that(best("TX", "heart attack"),
                    equals("CYPRESS FAIRBANKS MEDICAL CENTER"))
        expect_that(best("TX", "heart failure"),
                    equals("FORT DUNCAN MEDICAL CENTER"))
        expect_that(best("MD", "heart attack"),
                    equals("JOHNS HOPKINS HOSPITAL, THE"))
        expect_that(best("MD", "pneumonia"),
                    equals("GREATER BALTIMORE MEDICAL CENTER"))
})