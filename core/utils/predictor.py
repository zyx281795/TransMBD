"""
预测模型模块，用于预测失智症严重程度
"""
import numpy as np
import json
import os
from datetime import datetime
import random


class DementiaPredictor:
    """
    失智症预测器类：模拟基于TransMbD的失智症严重程度预测功能
    在实际应用中，这将通过Mistral 7B语言模型实现
    """
    
    def __init__(self):
        """初始化预测器"""
        # 定义失智症评估维度及其权重
        self.dimensions = {
            'memory': 0.30,
            'orientation': 0.25,
            'language': 0.20,
            'attention': 0.15,
            'problem_solving': 0.10
        }
        
        # 失智症严重程度阈值
        self.severity_thresholds = {
            'normal': (0.0, 0.2),
            'mild': (0.2, 0.5),
            'moderate': (0.5, 0.75),
            'severe': (0.75, 1.0)
        }
        
        # 创建一个简单的规则引擎来模拟LLM的判断
        self.rules = self._initialize_rules()
        
    def _initialize_rules(self):
        """初始化规则引擎"""
        # 在实际应用中，这些规则将由经过微调的LLM模型取代
        rules = {
            'memory': [
                {'pattern': '忘记', 'score': 0.6},
                {'pattern': '记不起来', 'score': 0.7},
                {'pattern': '想不起来', 'score': 0.65},
                {'pattern': '不记得', 'score': 0.55},
                {'pattern': '忘了', 'score': 0.5},
            ],
            'orientation': [
                {'pattern': '不知道现在是几点', 'score': 0.5},
                {'pattern': '不清楚今天日期', 'score': 0.6},
                {'pattern': '不知道这是哪里', 'score': 0.75},
                {'pattern': '迷失', 'score': 0.8},
                {'pattern': '迷惑', 'score': 0.7},
            ],
            'language': [
                {'pattern': '词不达意', 'score': 0.4},
                {'pattern': '表达困难', 'score': 0.5},
                {'pattern': '说不出来', 'score': 0.6},
                {'pattern': '词汇重复', 'score': 0.45},
                {'pattern': '句子不完整', 'score': 0.55},
            ],
            'attention': [
                {'pattern': '注意力不集中', 'score': 0.5},
                {'pattern': '容易分心', 'score': 0.4},
                {'pattern': '无法专注', 'score': 0.65},
                {'pattern': '思绪混乱', 'score': 0.7},
            ],
            'problem_solving': [
                {'pattern': '解决问题困难', 'score': 0.55},
                {'pattern': '逻辑混乱', 'score': 0.6},
                {'pattern': '无法理解简单问题', 'score': 0.8},
                {'pattern': '决策困难', 'score': 0.5},
            ]
        }
        return rules
    
    def _extract_features_from_text(self, text):
        """从文本中提取特征（简化版）"""
        # 在实际应用中，这将使用更复杂的NLP技术
        features = {}
        
        # 为每个维度计算一个基础分数
        for dimension, rules_list in self.rules.items():
            dimension_score = 0
            hits = 0
            
            for rule in rules_list:
                if rule['pattern'].lower() in text.lower():
                    dimension_score += rule['score']
                    hits += 1
            
            # 如果有匹配的规则，计算平均分
            if hits > 0:
                features[dimension] = dimension_score / hits
            else:
                # 基础噪声值，模拟模型的不确定性
                features[dimension] = 0.1
        
        return features
    
    def predict_from_text(self, text, patient_history=None):
        """
        根据文本内容预测失智症严重程度
        
        Args:
            text: 患者输入的文本
            patient_history: 患者历史评估信息（可选）
            
        Returns:
            prediction: 包含预测结果的字典
        """
        # 提取特征
        features = self._extract_features_from_text(text)
        
        # 根据历史数据调整预测（如果有）
        if patient_history and len(patient_history) > 0:
            features = self._adjust_with_history(features, patient_history)
        
        # 计算加权严重程度分数
        severity_score = 0
        for dimension, weight in self.dimensions.items():
            severity_score += features.get(dimension, 0.1) * weight
        
        # 确定严重程度类别
        severity_category = 'normal'
        for category, (lower, upper) in self.severity_thresholds.items():
            if lower <= severity_score < upper:
                severity_category = category
                break
        
        # 计算置信度（简化版）
        confidence = 0.5 + random.uniform(0, 0.4)  # 模拟置信度
        
        # 构建结果
        prediction = {
            'severity_score': round(severity_score, 2),
            'severity_category': severity_category,
            'confidence': round(confidence, 2),
            'dimension_scores': {k: round(v, 2) for k, v in features.items()},
            'timestamp': datetime.now().isoformat(),
        }
        
        return prediction
    
    def _adjust_with_history(self, current_features, history):
        """根据历史数据调整当前预测"""
        # 获取最近的历史评估
        if not history:
            return current_features
            
        # 计算历史趋势和变化率
        # 在实际应用中，这将是一个更复杂的时间序列分析
        trends = {}
        
        # 简单加权平均，偏向最近的评估
        adjusted_features = current_features.copy()
        for dimension in self.dimensions:
            if dimension in current_features:
                # 历史评估中该维度的平均值（如果存在）
                history_values = [h.get('dimension_scores', {}).get(dimension) 
                                 for h in history if dimension in h.get('dimension_scores', {})]
                
                if history_values:
                    # 计算加权平均值，最新的历史数据权重更大
                    weights = [i+1 for i in range(len(history_values))]
                    weighted_avg = sum(v * w for v, w in zip(history_values, weights)) / sum(weights)
                    
                    # 当前评估和历史趋势的混合
                    adjusted_features[dimension] = 0.7 * current_features[dimension] + 0.3 * weighted_avg
        
        return adjusted_features
    
    def generate_report(self, prediction, patient_info=None):
        """
        根据预测结果生成描述性报告
        
        Args:
            prediction: 预测结果字典
            patient_info: 患者基本信息字典（可选）
            
        Returns:
            report: 描述性报告字符串
        """
        severity = prediction['severity_category']
        score = prediction['severity_score']
        
        # 报告模板
        report_templates = {
            'normal': [
                "患者当前认知功能处于正常范围，未发现明显失智症状。",
                "患者思维清晰，记忆、语言及问题解决能力正常。",
                "评估显示患者认知功能良好，无需特别干预。"
            ],
            'mild': [
                "患者表现出轻度认知障碍，可能处于失智症早期阶段。",
                "患者在记忆和方向感方面有轻微困难，但日常功能基本正常。",
                "评估显示患者有轻度认知功能衰退，建议定期监测。"
            ],
            'moderate': [
                "患者表现出中度失智症状，认知功能明显下降。",
                "患者在记忆、语言表达和日常决策方面存在显著困难。",
                "评估显示患者认知能力中度受损，需要适当照护支持。"
            ],
            'severe': [
                "患者表现出严重失智症状，认知功能严重受损。",
                "患者在大多数认知领域表现出显著困难，需要全面照护。",
                "评估显示患者处于失智症晚期阶段，需要专业护理支持。"
            ]
        }
        
        # 随机选择一个模板
        base_report = random.choice(report_templates[severity])
        
        # 添加维度特定的观察
        dimension_observations = []
        for dimension, score in prediction['dimension_scores'].items():
            if dimension == 'memory' and score > 0.5:
                dimension_observations.append(f"患者记忆力受损明显，表现为短期记忆困难。")
            elif dimension == 'orientation' and score > 0.5:
                dimension_observations.append(f"患者在时间和空间定向方面表现出困难。")
            elif dimension == 'language' and score > 0.5:
                dimension_observations.append(f"患者语言表达能力下降，词汇查找和句子构建困难。")
            elif dimension == 'attention' and score > 0.5:
                dimension_observations.append(f"患者注意力难以集中，容易分心。")
            elif dimension == 'problem_solving' and score > 0.5:
                dimension_observations.append(f"患者解决问题的能力下降，思维逻辑受损。")
        
        # 拼接报告
        full_report = base_report
        if dimension_observations:
            full_report += "\n\n具体观察：\n" + "\n".join(dimension_observations)
        
        # 添加建议
        if severity == 'normal':
            full_report += "\n\n建议：保持健康生活方式，定期认知功能检查。"
        elif severity == 'mild':
            full_report += "\n\n建议：增加认知刺激活动，考虑专业医疗评估，定期监测认知变化。"
        elif severity == 'moderate':
            full_report += "\n\n建议：寻求专业医疗干预，制定照护计划，确保安全环境。"
        else:  # severe
            full_report += "\n\n建议：需要专业全天候照护，制定详细照护方案，关注生活质量。"
        
        return full_report


class ConversationManager:
    """管理与患者的对话交互"""
    
    def __init__(self, predictor=None):
        """初始化对话管理器"""
        self.predictor = predictor or DementiaPredictor()
        
        # 常见问题模板
        self.question_templates = [
            "您能告诉我今天是几月几号吗？",
            "您现在住在哪里？可以描述一下您的住所吗？",
            "您能回忆一下您今天早上做了什么吗？",
            "您能告诉我您最近一次看医生是什么时候吗？",
            "请描述一下您现在的心情。",
            "您最喜欢的食物是什么？为什么喜欢？",
            "您能告诉我您年轻时的一个美好回忆吗？",
            "您平时有什么爱好或兴趣吗？",
            "您能说说您的家人吗？您有几个孩子？",
            "如果您遇到困难，通常会怎么解决？",
        ]
        
        # 积极回应和引导模板
        self.response_templates = {
            'acknowledgment': [
                "谢谢您的回答。",
                "我明白了。",
                "感谢您分享这些信息。",
                "好的，我了解了。",
            ],
            'encouragement': [
                "您分享的内容很有帮助。",
                "请继续，您做得很好。",
                "您的回答非常清晰。",
                "非常感谢您的耐心。",
            ],
            'follow_up': [
                "能再多告诉我一些吗？",
                "有什么其他想法吗？",
                "还有什么您想分享的吗？",
                "您能多描述一点细节吗？",
            ]
        }
    
    def generate_question(self, context=None):
        """生成适合当前对话上下文的问题"""
        # 简单随机选择一个问题模板
        # 在实际应用中，这将基于对话历史和患者状态更智能地选择
        return random.choice(self.question_templates)
    
    def generate_response(self, patient_input, conversation_history=None):
        """
        根据患者输入生成回应
        
        Args:
            patient_input: 患者的输入文本
            conversation_history: 对话历史列表
            
        Returns:
            response: 系统回应
            assessment: 基于患者输入的评估结果
        """
        # 预测患者状态
        assessment = self.predictor.predict_from_text(patient_input)
        
        # 构建回应
        acknowledgment = random.choice(self.response_templates['acknowledgment'])
        
        # 基于评估结果调整回应的复杂性
        if assessment['severity_category'] in ['moderate', 'severe']:
            # 对于中度或重度患者，使用更简单的语言
            encouragement = random.choice([
                "您做得很好。",
                "谢谢您的回答。",
                "您的分享很重要。"
            ])
            
            # 生成一个简单的后续问题
            next_question = random.choice([
                "您能告诉我您的感受吗？",
                "您现在感觉如何？",
                "您能描述一下您看到的东西吗？",
                "您能告诉我现在是什么时间吗？"
            ])
        else:
            # 对于正常或轻度患者，可以使用更复杂的语言
            encouragement = random.choice(self.response_templates['encouragement'])
            
            # 生成一个后续问题
            next_question = self.generate_question()
        
        # 组合回应
        response = f"{acknowledgment} {encouragement}\n\n{next_question}"
        
        return response, assessment
