library(tidyverse)

d <- read_csv("facebook-accounts-from-district-homepages.csv")

files <- list.files("data")

link_proc_from_files <- str_split(files, ".csv") %>% 
  map_chr(~.[1]) %>% 
  as_tibble() %>% 
  set_names("link_proc") %>% 
  mutate(status = "accessed")

d %>% 
  left_join(link_proc_from_files) %>% 
  janitor::tabyl(status)

log1 <- read_lines("logs/2020-09-15-error-log-running-all-first-half.txt")
log2 <- read_lines("logs/2020-09-15-error-log-running-all-second-half.txt")

log <- c(log1, log2)

log <- log %>% 
  as_tibble() %>% 
  separate(value, into = c("link_proc", "status"), sep = " - ") 

log %>% 
  count(status)

# link_to_incomplete_files <- log %>% 
#   filter(status == "incomplete") %>% 
#   mutate(link_to_file = str_c(link_proc, ".csv")) %>% 
#   pull(link_to_file)
# 
# incomplete_files_list <- files[files %in% link_to_incomplete_files] %>% 
#   str_c("data/", .) %>% 
#   map(read_csv)

read_files_list <- files %>% 
  str_c("data/", .) %>% 
  map(read_csv)

create_new_id_column <- function(d, file_name) {
  
  
  d %>% 
    select(-X1) %>% 
    mutate(file_name = file_name) %>% 
    mutate(comments = as.integer(comments)) %>% 
    mutate(likes = as.integer(likes)) %>% 
    mutate(shares = as.integer(shares)) %>% 
    mutate(time = as.character(time)) %>% 
    mutate(post_id = as.character(post_id)) %>% 
    mutate(video_thumbnail = as.character(video_thumbnail)) %>% 
    rename(link_proc = file_name)
  
}

large_df <- map2_df(read_files_list, files, ~create_new_id_column(.x, .y))
