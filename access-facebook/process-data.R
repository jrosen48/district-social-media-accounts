library(tidyverse)
library(lubridate)

d <- read_csv("facebook-accounts-from-district-homepages.csv")
nces_info_for_districts <- read_csv("facebook/nces-info-for-districts.csv")

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

large_df_unprocessed <- map2_df(read_files_list, files, ~create_new_id_column(.x, .y))

just_nces_id_and_website <- nces_info_for_districts %>% 
  select(link_proc, url, nces_id)

large_df <- large_df_unprocessed %>% 
  mutate(link_proc = str_split(link_proc, ".csv")) %>% 
  mutate(link_proc = map_chr(link_proc, ~.[[1]])) %>% 
  left_join(just_nces_id_and_website) %>% 
  select(-video, -video_thumbnail)

write_csv(large_df, "processed-joined-facebook-data.csv")

large_df <- read_csv("processed-joined-facebook-data.csv")

large_df <- large_df %>% 
  mutate(time = lubridate::ymd_hms(time),
         time_r = lubridate::round_date(time, "day"))

large_df %>% 
  count(time_r) %>% 
  filter(time_r > lubridate::ymd("2020-01-01")) %>% 
  mutate(wday = lubridate::wday(time_r, label = TRUE)) %>% 
  group_by(wday) %>% 
  summarize(sum_wday = sum(n)) %>% 
  ggplot(aes(x = wday, y = sum_wday)) +
  geom_col()

large_df %>% 
  count(time_r) %>% 
  filter(time_r > lubridate::ymd("2020-01-01")) %>% 
  ggplot(aes(x = time_r, y = n)) +
  geom_col() +
  hrbrthemes::theme_ipsum()

p <- large_df %>% 
  mutate(closure = str_detect(tolower(text), "clos*")) %>% 
  filter(time_r > lubridate::ymd("2020-01-01")) %>%
  count(closure, time_r) %>% 
  filter(closure) %>% 
  ggplot(aes(x = time_r, y = n)) +
  geom_point() +
  geom_line() +
  hrbrthemes::theme_ipsum() +
  ggtitle("Mentions of closures")

large_df %>% 
  mutate(st = str_detect(tolower(text), "st math") |
           str_detect(tolower(text), "stmath")) %>% 
  count(st)
