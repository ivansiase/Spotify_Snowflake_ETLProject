# 🎵 Spotify Data Pipeline with AWS & Snowflake

This project demonstrates a modern data engineering pipeline that integrates the Spotify API, processes data with Python, deploys it using AWS Lambda, and automates ingestion into Snowflake using Snowpipe.

---

## 🚀 Project Overview

This pipeline automates the process of extracting data from Spotify, transforming it in Python, and ingesting it into Snowflake for further analysis.

### ✅ Key Components

- **Spotify API Integration**: Extracts music-related data (e.g. tracks, playlists, artists).
- **AWS Lambda**: Hosts the Python script to automate extraction and transformation.
- **AWS CloudWatch Trigger**: Automatically invokes the Lambda function on a schedule.
- **Amazon S3**: Stores the transformed data files (.csv or .json).
- **Snowpipe**: Automatically ingests the files from S3 into Snowflake.

---

## 🛠️ Technologies Used

- **Programming**: Python 3
- **Cloud Services**: AWS Lambda, S3, IAM, CloudWatch
- **Data Warehouse**: Snowflake
- **Data Integration**: Spotify Web API, Snowpipe
- **Others**: boto3, requests

---

## 📁 Project Structure

```plaintext
spotify-data-pipeline/
├── AWS lambda/
│   ├── Extract_Spotify_Data.py
│   └── Transform_Spotify_Data.py
├── snowflake/
│   ├── Snowflake_SQL.sql
│   └── Storage_Integration.sql
├── S3-Sample-Output/
├── raw-data/                         ← stores unprocessed data pulled from Spotify API
│   ├── processed/
│   └── to_process/
├── transform-data/                   ← stores cleaned, transformed datasets ready for loading into Snowflake
│   ├── album_data/
│   ├── artist_data/
│   └── songs_data/

```


## 📽️ Demo Video

You can watch the demo video here: [Spotify_Pipeline.mkv](assets/Spotify_Pipeline.mkv)



---

## 📚 Acknowledgement

This project was inspired by the "Data Warehouse for Data Engineering with Snowflake" by [Darshil Parmar](https://www.linkedin.com/in/darshilparmar/). The course provided the foundational concepts and structure for integrating Spotify, AWS, and Snowflake.

All implementation, customization, and additional enhancements in this repository are my own work and reflect my personal understanding and learning.


