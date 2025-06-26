from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
import os
from django.core.files import File
from meetings.models import Meeting, AgendaItem, Attachment
from datetime import timedelta, datetime

# 定義 Command 類別，負責生成假數據
class Command(BaseCommand):
    help = '生成指定語言的會議、議程和附件假數據。'  # 幫助信息

    def add_arguments(self, parser):
        # 添加參數：會議數量和語言選擇
        parser.add_argument('--num_meetings', type=int, default=5, help='要生成的會議數量')
        parser.add_argument('--language', type=str, default='all', choices=['en', 'zh', 'tw', 'all'],
                            help='假數據語言：en 為英文，zh 為簡體中文，tw 為繁體中文，all 為所有語言')

    def handle(self, *args, **options):
        num_meetings = options['num_meetings']  # 獲取會議數量
        language = options['language'].lower()  # 獲取語言設定

        # 初始化 Faker 实例，根據語言選擇
        if language == 'all':
            faker_en = Faker('en_US')  # 英文實例
            faker_zh = Faker('zh_CN')  # 簡體中文實例
            faker_tw = Faker('zh_TW')  # 繁體中文實例
        else:
            faker = Faker({
                'en': 'en_US',  # 英文
                'zh': 'zh_CN',  # 簡體中文
                'tw': 'zh_TW'   # 繁體中文
            }.get(language, 'en_US'))

        for i in range(num_meetings):
            # 根據語言模式選擇當前 Faker 實例
            if language == 'all':
                if i % 3 == 0:
                    current_faker = faker_en  # 每第三個為英文
                elif i % 3 == 1:
                    current_faker = faker_zh  # 每第二個為簡體中文
                else:
                    current_faker = faker_tw  # 每第一個為繁體中文
            else:
                current_faker = faker  # 使用單一語言實例

            # 獲取日期和時間
            meeting_date = current_faker.date_this_year()
            start_time = current_faker.time_object()
            # 將時間與日期結合，然後加時間差
            start_datetime = datetime.combine(meeting_date, start_time)
            end_datetime = start_datetime + timedelta(hours=2)

            # 生成參加人名單，使用 name() 多次呼叫
            attendee_names = [current_faker.name() for _ in range(3)]  # 生成3個名稱
            attendees = ", ".join(attendee_names)

            # 創建假會議數據
            meeting = Meeting.objects.create(
                title=current_faker.sentence()[:190],  # 限制標題長度，留10字元緩衝
                date=meeting_date,  # 使用結合的日期
                start_time=start_time,  # 使用原始時間
                end_time=end_datetime.time(),  # 提取時間部分
                location=current_faker.city()[:90],  # 限制地點長度，留10字元緩衝
                attendees=attendees,  # 使用生成的參加人名單
                minutes=current_faker.paragraph()  # 生成會議記錄
            )

            # 為每個會議創建假議程
            for j in range(3):
                AgendaItem.objects.create(
                    meeting=meeting,
                    item_number=j + 1,
                    item_title=current_faker.sentence()[:190],  # 限制議程標題長度
                    description=current_faker.paragraph(),
                    responsible_person=current_faker.name()[:90],  # 限制負責人名稱長度
                    estimated_time=timedelta(minutes=current_faker.random_int(min=10, max=30))
                )

            # 創建假附件
            # 創建有意義的檔案名稱：日期_會議標題_附件
            date_str = meeting_date.strftime('%Y%m%d')
            title_slug = slugify(meeting.title)[:30]  # 限制標題長度，避免檔名過長
            meaningful_filename = f"{date_str}_{title_slug}_attachment.txt"
            
            temp_file = f"temp_{current_faker.uuid4()}.txt"  # 臨時文件名稱
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(current_faker.text())  # 寫入假文本
            with open(temp_file, 'rb') as f:
                attachment = Attachment.objects.create(
                    meeting=meeting,
                    file=File(f, name=meaningful_filename)
                )
            os.remove(temp_file)  # 清理臨時文件

        # 定義語言描述字典
        lang_desc = {
            'en': 'English',  # 英文描述
            'zh': 'Simplified Chinese',  # 簡體中文描述
            'tw': 'Traditional Chinese',  # 繁體中文描述
            'all': 'all languages'  # 所有語言描述
        }
        self.stdout.write(self.style.SUCCESS(f'成功生成了 {num_meetings} 個 {lang_desc[language]} 會議'))  # 輸出成功訊息
# 使用 Faker 生成會議應用的假數據
# 此命令可以使用以下方式運行：python manage.py generate_fake_data()
# 此腳本為 Meeting、AgendaItem 和 Attachment 模型生成假數據。
# 此命令可以使用以下方式運行：python manage.py generate_fake_data --num_meetings 10
# 它將創建 10 個假會議，每個會議有 3 個議程項目和一個附件。
# 通過更改 --num_meetings 參數來調整會議數量。
# 確保在您的環境中安裝了 Faker 庫。
# 您可以使用 pip 安裝：pip install Faker

# 更新: 現在支持多語言
# 此命令現在支持生成英文、簡體中文、繁體中文或所有語言的數據。
# 使用 --language 參數來指定所需的語言。
# python manage.py generate_fake_data --num_meetings 5 --language en
# python manage.py generate_fake_data --num_meetings 5 --language zh
