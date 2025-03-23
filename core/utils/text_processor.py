"""
文本处理模块，用于分析患者输入的文本并提取特征
"""
import re
import numpy as np
from collections import Counter


class TextProcessor:
    def __init__(self):
        """初始化文本处理器"""
        # 常见语言错误和混乱模式的正则表达式
        self.patterns = {
            'repetition': r'(\b\w+\b)(\s+\1\b)+',
            'incomplete_sentence': r'[^.!?]+[.!?]*$',
            'filler_words': r'\b(嗯|呃|那个|这个|就是|然后)\b',
            'hesitation': r'\.{3,}',
            'confused_reference': r'\b(那個|那个东西|那个人|那件事)\b',
        }
        
        # 失智症相关的语义指标词汇库
        self.semantic_indicators = {
            'time_disorientation': ['昨天', '今天', '明天', '上周', '下周', '几点', '什么时候', '日期'],
            'place_disorientation': ['这里', '那里', '在哪里', '这是哪里', '回家', '医院'],
            'memory_issue': ['忘了', '记不起来', '想不起来', '不记得', '记得', '前几天'],
        }
    
    def preprocess_text(self, text):
        """预处理文本"""
        # 转为小写
        text = text.lower()
        
        # 移除多余空格
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 移除特殊字符（保留标点符号）
        text = re.sub(r'[^\w\s,.!?;:，。！？；：]', '', text)
        
        return text
    
    def extract_features(self, text):
        """从文本中提取潜在的失智症语言特征"""
        preprocessed_text = self.preprocess_text(text)
        features = {}
        
        # 文本基本统计特征
        features['word_count'] = len(preprocessed_text.split())
        features['char_count'] = len(preprocessed_text)
        features['sentence_count'] = len(re.split(r'[.!?。！？]', preprocessed_text)) - 1
        
        if features['sentence_count'] <= 0:
            features['sentence_count'] = 1
        
        features['avg_words_per_sentence'] = features['word_count'] / features['sentence_count']
        
        # 分析语言错误模式
        for pattern_name, pattern in self.patterns.items():
            matches = re.findall(pattern, preprocessed_text)
            features[f'{pattern_name}_count'] = len(matches)
        
        # 分析语义指标
        for category, keywords in self.semantic_indicators.items():
            count = sum(1 for keyword in keywords if keyword in preprocessed_text)
            features[f'{category}_score'] = count
        
        # 词汇多样性（不同词汇占总词汇的比例）
        words = preprocessed_text.split()
        if words:
            features['lexical_diversity'] = len(set(words)) / len(words)
        else:
            features['lexical_diversity'] = 0
            
        # 代词使用比例
        pronouns = ['我', '你', '他', '她', '它', '我們', '你們', '他們', '她們', '它們',
                    '这个', '那个', '这些', '那些']
        pronoun_count = sum(1 for word in words if word in pronouns)
        features['pronoun_ratio'] = pronoun_count / max(1, features['word_count'])
        
        return features
    
    def analyze_response_coherence(self, question, answer):
        """分析问题与回答之间的连贯性"""
        # 这里简化了分析逻辑，实际应用中可能需要更复杂的自然语言处理
        question_keywords = set(self.preprocess_text(question).split())
        answer_keywords = set(self.preprocess_text(answer).split())
        
        # 计算问题和回答之间的词汇重叠度
        overlap = question_keywords.intersection(answer_keywords)
        overlap_ratio = len(overlap) / max(1, len(question_keywords))
        
        # 回答是否包含实质性内容（不仅仅是"不知道"之类的回应）
        substantive_response = not all(word in ['不知道', '忘了', '记不起来', '不记得'] 
                                     for word in answer_keywords)
        
        return {
            'overlap_ratio': overlap_ratio,
            'substantive_response': substantive_response,
            'response_length': len(answer_keywords)
        }
    
    def compute_language_decline_indicators(self, text_samples):
        """
        计算一系列文本样本中可能表明语言能力下降的指标
        
        Args:
            text_samples: 时间序列排序的文本样本列表
            
        Returns:
            decline_metrics: 语言能力下降指标的字典
        """
        if not text_samples or len(text_samples) < 2:
            return {'sufficient_data': False}
        
        # 提取每个样本的特征
        features_over_time = [self.extract_features(text) for text in text_samples]
        
        # 计算关键指标随时间的变化
        decline_metrics = {
            'sufficient_data': True,
            'lexical_diversity_change': self._compute_trend([f['lexical_diversity'] for f in features_over_time]),
            'sentence_length_change': self._compute_trend([f['avg_words_per_sentence'] for f in features_over_time]),
            'repetition_change': self._compute_trend([f['repetition_count'] for f in features_over_time]),
            'confusion_change': self._compute_trend([
                f['confused_reference_count'] for f in features_over_time
            ]),
        }
        
        # 汇总变化指标以得出总体下降评分
        negative_indicators = [
            v for k, v in decline_metrics.items() 
            if k.endswith('_change') and ((k.startswith('repetition') or k.startswith('confusion')) and v > 0 
                                       or (not k.startswith('repetition') and not k.startswith('confusion')) and v < 0)
        ]
        
        if negative_indicators:
            decline_metrics['overall_decline_score'] = sum(negative_indicators) / len(negative_indicators)
        else:
            decline_metrics['overall_decline_score'] = 0
            
        return decline_metrics
    
    def _compute_trend(self, values):
        """
        计算数值序列的趋势斜率
        正值表示上升趋势，负值表示下降趋势
        """
        if not values or len(values) < 2:
            return 0
            
        x = np.array(range(len(values)))
        y = np.array(values)
        
        # 简单线性回归得到斜率
        slope = np.polyfit(x, y, 1)[0]
        return slope
