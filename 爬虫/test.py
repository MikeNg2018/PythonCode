def make_url_list(u_link, total_pages):
    # 以c_p为分隔符拆分URL
    sp = u_link.split('c_p')
    u_link_part1 = sp[0]
    u_link_part2 = sp[1]

    # 第二部分以/分隔，提取第二部分
    page_split = u_link_part2.split('/')
    url_end_part = page_split[1]

    # 创建空列表存放处理后的URL
    all_url = []

    # 总页数从外部传入，生成以第二页开始，总页数为止的URL，存入列表
    for pages in range(2, total_pages+1):
        finall_url = "{}{}{}{}{}".format(u_link_part1, "c_p", pages, "/", url_end_part)
        all_url.append(finall_url)
        # print(finall_url)

    # print(all_url)