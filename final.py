import re

def insert_translations_to_srt(srt_file, translation_file, output_file):
    """
    将翻译后的中文文本插入到原版字幕文件中，生成中英双语字幕
    :param srt_file: 原版字幕文件路径
    :param translation_file: 翻译后的中文文本文件路径
    :param output_file: 输出的双语字幕文件路径
    """
    # 读取原版字幕文件
    with open(srt_file, "r", encoding="utf-8") as f:
        srt_lines = f.readlines()

    # 读取翻译后的中文文本文件
    with open(translation_file, "r", encoding="utf-8") as f:
        translations = f.read().strip().split("\n")

    # 提取英文字幕内容
    english_subtitles = []
    for line in srt_lines:
        if not re.match(r"^\d+$", line.strip()) and not re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line.strip()) and line.strip():
            english_subtitles.append(line.strip())

    # 检查中英字幕数量是否一致
    if len(english_subtitles) != len(translations):
        raise ValueError("英文字幕与中文翻译数量不一致，请检查翻译文本是否完整！")

    # 插入中文翻译到原版字幕文件
    bilingual_lines = []
    translation_index = 0
    for line in srt_lines:
        if re.match(r"^\d+$", line.strip()) or re.match(r"(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})", line.strip()):
            # 保留数字行和时间轴行
            bilingual_lines.append(line)
        elif line.strip():
            # 插入中文翻译和英文字幕
            bilingual_lines.append(f"{translations[translation_index]}\n")
            bilingual_lines.append(f"{line.strip()}\n")
            translation_index += 1
        else:
            # 保留空行
            bilingual_lines.append(line)

    # 保存双语字幕文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(bilingual_lines)

    print(f"双语字幕生成完成！文件已保存到 {output_file}")

# 使用脚本
insert_translations_to_srt("字幕文本.srt", "翻译文本.txt", "双语字幕.srt")