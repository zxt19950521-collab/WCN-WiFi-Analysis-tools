import pandas as pd
import os
import json

class TagProcessor:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.tags = []
    
    def read_excel(self):
        """读取Excel文件并提取TAG信息"""
        try:
            # 读取Excel文件
            df = pd.read_excel(self.excel_file)
            
            # 假设TAG信息在第一列
            for index, row in df.iterrows():
                # 提取非空的TAG
                for col in df.columns:
                    tag = str(row[col]).strip()
                    if tag and tag != 'nan':
                        self.tags.append(tag)
            
            # 去重
            self.tags = list(set(self.tags))
            print(f"成功提取 {len(self.tags)} 个TAG")
            return True
        except Exception as e:
            print(f"读取Excel文件失败: {e}")
            return False
    
    def generate_tag_config(self):
        """生成TAG配置文件"""
        tag_config = {
            "tags": self.tags,
            "version": "1.0",
            "description": "WiFi故障分析TAG配置"
        }
        
        # 保存配置文件
        config_path = os.path.join(os.path.dirname(self.excel_file), "tag_config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(tag_config, f, ensure_ascii=False, indent=2)
        
        print(f"TAG配置文件已保存到: {config_path}")
        return config_path
    
    def integrate_with_skill(self):
        """将TAG集成到现有技能中"""
        # 读取现有的SKILL.md文件
        skill_file = os.path.join(os.path.dirname(self.excel_file), "SKILL.md")
        
        if not os.path.exists(skill_file):
            print(f"SKILL.md文件不存在: {skill_file}")
            return False
        
        # 读取SKILL.md内容
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 在关键日志分析部分添加TAG信息
        tag_section = "\n### TAG分类\n"
        for tag in self.tags:
            tag_section += f"- `{tag}`\n"
        
        # 找到关键日志分析部分并插入TAG信息
        if "## 关键日志分析" in content:
            new_content = content.replace("## 关键日志分析", f"## 关键日志分析{tag_section}")
            
            # 保存更新后的SKILL.md
            with open(skill_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("TAG信息已成功集成到SKILL.md")
            return True
        else:
            print("SKILL.md文件中未找到关键日志分析部分")
            return False
    
    def process(self):
        """处理整个流程"""
        if self.read_excel():
            self.generate_tag_config()
            self.integrate_with_skill()
            return True
        return False

if __name__ == "__main__":
    # 处理Excel文件
    excel_file = "d:\\AI\\Wifi-analysis\\WCN-WiFi-Analysis-tools\\WIFI问题分析红宝书.xlsx"
    processor = TagProcessor(excel_file)
    processor.process()
