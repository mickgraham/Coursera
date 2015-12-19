list.files("diet_data")

andy <- read.csv("diet_data/Andy.csv")

head(andy)
length(andy$Day)
dim(andy)
str(andy)
summary(andy)
names(andy)

andy[1, "Weight"]
andy[30, "Weight"]

# subset of the ‘Weight’ column where the data where ‘Day’ is equal to 30.
andy[which(andy$Day == 30), "Weight"]
andy[which(andy[,"Day"] == 30), "Weight"]
subset(andy$Weight, andy$Day==30)

# Assign Andy’s starting and ending weight to vectors.
#Find out how much weight he lost by subtracting the vectors.
andy_start <- andy[1, "Weight"]
andy_end <- andy[30, "Weight"]
andy_loss <- andy_start - andy_end
andy_loss

# Now let’s try taking a look at John.csv.
files_full <- list.files("diet_data", full.names=TRUE)
head(read.csv(files_full[3]))

#Add David's rows to Andy's.
andy_david <- rbind(andy, read.csv(files_full[2]))
andy_david

# Create a subset of the data frame that shows the 25th day for Andy and David.
day_25 <- andy_david[which(andy_david$Day == 25), ]
day_25

# Create one big data frame with everybody’s data in it.
dat <- data.frame()
for (i in 1:5) {
        dat <- rbind(dat, read.csv(files_full[i]))
}
str(dat)
dat

# The median weight for day 30.
median(dat$Weight)
dat_30 <- dat[which(dat[, "Day"] == 30),]
median(dat_30$Weight)

?median

# Function that will return the median weight of a given day.
weightmedian <- function(directory, day) {
        # creates a list of files
        files_list <- list.files(directory, full.names=TRUE)
        #creates an empty data frame
        dat <- data.frame()
        #loops through the files, rbinding them together
        for (i in 1:5) {
                dat <- rbind(dat, read.csv(files_list[i]))
        }
        #subsets the rows that match the 'day' argument
        dat_subset <- dat[which(dat[, "Day"] == day),]
        #identifies the median of the subset while stripping out the NAs
        median(dat_subset$Weight, na.rm=TRUE)
}