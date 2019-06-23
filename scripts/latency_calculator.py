LATENCY_FILE_LOCATION = "../receivers/latency.txt"

if __name__ == '__main__':
    average_latency = 0
    count = 0
    with open(LATENCY_FILE_LOCATION, mode="rt") as file_handler:
        for line in file_handler:
            latency = line.strip()
            if not latency:
                continue

            average_latency += float(latency)
            count += 1

    average_latency /= count
    print(average_latency)
