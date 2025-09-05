"""
ScamShield AI-A - Model Performance Optimizer
Advanced system for optimizing model selection and performance
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import logging
import numpy as np
from dataclasses import dataclass
from collections import defaultdict
import statistics

@dataclass
class ModelPerformanceMetrics:
    """Performance metrics for AI models"""
    model_name: str
    accuracy_score: float
    response_time: float
    cost_per_request: float
    success_rate: float
    confidence_calibration: float
    specialization_performance: Dict[str, float]
    user_satisfaction: float
    error_rate: float

@dataclass
class OptimizationTarget:
    """Optimization targets for model selection"""
    max_cost_per_investigation: float
    min_accuracy_threshold: float
    max_response_time: int
    priority_weights: Dict[str, float]  # accuracy, cost, speed, satisfaction

class ModelPerformanceOptimizer:
    """
    Advanced optimizer for model performance and cost-effectiveness
    """
    
    def __init__(self):
        self.optimizer_id = "MODEL_PERFORMANCE_OPTIMIZER_001"
        self.performance_history = defaultdict(list)
        self.optimization_rules = self._initialize_optimization_rules()
        self.learning_rate = 0.1
        self.performance_window = timedelta(days=7)
        
    def _initialize_optimization_rules(self) -> Dict[str, Any]:
        """Initialize optimization rules and thresholds"""
        return {
            "accuracy_thresholds": {
                "critical_investigations": 0.95,
                "high_priority": 0.90,
                "standard": 0.85,
                "screening": 0.80
            },
            "cost_efficiency_targets": {
                "ultra_premium": 0.030,  # Max cost per 1k tokens
                "premium": 0.015,
                "high_performance": 0.006,
                "standard": 0.001,
                "efficient": 0.0002
            },
            "response_time_targets": {
                "emergency": 30,      # seconds
                "urgent": 60,
                "priority": 120,
                "standard": 300,
                "batch": 600
            },
            "model_switching_thresholds": {
                "accuracy_drop": 0.05,
                "cost_increase": 0.20,
                "response_time_increase": 0.30,
                "error_rate_increase": 0.10
            },
            "ensemble_optimization": {
                "min_agreement_threshold": 0.80,
                "max_models_per_ensemble": 3,
                "confidence_boost_threshold": 0.15,
                "cost_efficiency_weight": 0.30
            }
        }
        
    async def optimize_model_selection(self, 
                                     investigation_requirements: Dict[str, Any],
                                     available_models: List[str],
                                     optimization_target: OptimizationTarget) -> Dict[str, Any]:
        """
        Optimize model selection based on requirements and performance history
        """
        optimization_id = f"OPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Analyze historical performance
        performance_analysis = await self._analyze_historical_performance(available_models)
        
        # Calculate model scores
        model_scores = await self._calculate_model_scores(
            available_models, investigation_requirements, optimization_target, performance_analysis
        )
        
        # Select optimal model configuration
        optimal_config = await self._select_optimal_configuration(
            model_scores, optimization_target
        )
        
        # Generate optimization recommendations
        recommendations = await self._generate_optimization_recommendations(
            optimal_config, performance_analysis
        )
        
        return {
            "optimization_id": optimization_id,
            "optimal_configuration": optimal_config,
            "model_scores": model_scores,
            "performance_analysis": performance_analysis,
            "recommendations": recommendations,
            "expected_performance": self._predict_performance(optimal_config),
            "cost_benefit_analysis": self._calculate_cost_benefit(optimal_config, optimization_target)
        }
        
    async def _analyze_historical_performance(self, models: List[str]) -> Dict[str, Any]:
        """Analyze historical performance data for models"""
        
        analysis = {}
        current_time = datetime.now()
        cutoff_time = current_time - self.performance_window
        
        for model in models:
            model_history = [
                metric for metric in self.performance_history[model]
                if metric.get("timestamp", current_time) >= cutoff_time
            ]
            
            if not model_history:
                # Use default metrics for new models
                analysis[model] = self._get_default_metrics(model)
                continue
                
            # Calculate performance statistics
            accuracy_scores = [m["accuracy"] for m in model_history if "accuracy" in m]
            response_times = [m["response_time"] for m in model_history if "response_time" in m]
            costs = [m["cost"] for m in model_history if "cost" in m]
            success_rates = [m["success"] for m in model_history if "success" in m]
            
            analysis[model] = {
                "avg_accuracy": statistics.mean(accuracy_scores) if accuracy_scores else 0.85,
                "accuracy_std": statistics.stdev(accuracy_scores) if len(accuracy_scores) > 1 else 0.05,
                "avg_response_time": statistics.mean(response_times) if response_times else 60,
                "response_time_std": statistics.stdev(response_times) if len(response_times) > 1 else 10,
                "avg_cost": statistics.mean(costs) if costs else 0.01,
                "cost_std": statistics.stdev(costs) if len(costs) > 1 else 0.002,
                "success_rate": statistics.mean(success_rates) if success_rates else 0.95,
                "sample_size": len(model_history),
                "trend_analysis": self._analyze_performance_trends(model_history),
                "reliability_score": self._calculate_reliability_score(model_history)
            }
            
        return analysis
        
    async def _calculate_model_scores(self, 
                                    models: List[str],
                                    requirements: Dict[str, Any],
                                    target: OptimizationTarget,
                                    performance_data: Dict[str, Any]) -> Dict[str, float]:
        """Calculate optimization scores for each model"""
        
        scores = {}
        weights = target.priority_weights
        
        for model in models:
            perf = performance_data.get(model, {})
            
            # Accuracy score (0-1)
            accuracy_score = min(perf.get("avg_accuracy", 0.85) / target.min_accuracy_threshold, 1.0)
            
            # Cost score (inverse - lower cost = higher score)
            avg_cost = perf.get("avg_cost", 0.01)
            cost_score = max(0, 1 - (avg_cost / target.max_cost_per_investigation))
            
            # Speed score (inverse - faster = higher score)
            avg_time = perf.get("avg_response_time", 60)
            speed_score = max(0, 1 - (avg_time / target.max_response_time))
            
            # Reliability score
            reliability_score = perf.get("reliability_score", 0.85)
            
            # Specialization match score
            specialization_score = self._calculate_specialization_match(
                model, requirements.get("investigation_type", "general")
            )
            
            # Weighted composite score
            composite_score = (
                weights.get("accuracy", 0.3) * accuracy_score +
                weights.get("cost", 0.25) * cost_score +
                weights.get("speed", 0.2) * speed_score +
                weights.get("reliability", 0.15) * reliability_score +
                weights.get("specialization", 0.1) * specialization_score
            )
            
            scores[model] = {
                "composite_score": composite_score,
                "accuracy_score": accuracy_score,
                "cost_score": cost_score,
                "speed_score": speed_score,
                "reliability_score": reliability_score,
                "specialization_score": specialization_score,
                "recommendation_confidence": self._calculate_recommendation_confidence(perf)
            }
            
        return scores
        
    async def _select_optimal_configuration(self, 
                                          model_scores: Dict[str, Dict[str, float]],
                                          target: OptimizationTarget) -> Dict[str, Any]:
        """Select optimal model configuration"""
        
        # Sort models by composite score
        sorted_models = sorted(
            model_scores.items(), 
            key=lambda x: x[1]["composite_score"], 
            reverse=True
        )
        
        # Primary model selection
        primary_model = sorted_models[0][0]
        primary_score = sorted_models[0][1]
        
        # Secondary model for validation (if beneficial)
        secondary_model = None
        if len(sorted_models) > 1:
            second_best = sorted_models[1]
            # Use secondary if it adds significant value
            if (second_best[1]["composite_score"] > 0.8 and 
                abs(primary_score["composite_score"] - second_best[1]["composite_score"]) < 0.1):
                secondary_model = second_best[0]
                
        # Ensemble configuration
        ensemble_config = self._configure_ensemble(primary_model, secondary_model, model_scores)
        
        return {
            "primary_model": primary_model,
            "secondary_model": secondary_model,
            "ensemble_configuration": ensemble_config,
            "expected_accuracy": self._calculate_expected_accuracy(ensemble_config),
            "expected_cost": self._calculate_expected_cost(ensemble_config),
            "expected_response_time": self._calculate_expected_response_time(ensemble_config),
            "confidence_level": primary_score["recommendation_confidence"],
            "optimization_rationale": self._generate_optimization_rationale(
                primary_model, model_scores, target
            )
        }
        
    def _configure_ensemble(self, 
                          primary: str, 
                          secondary: Optional[str], 
                          scores: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Configure ensemble based on selected models"""
        
        config = {
            "type": "single" if not secondary else "dual",
            "models": [primary],
            "weights": [1.0],
            "voting_strategy": "weighted_average",
            "confidence_threshold": 0.85
        }
        
        if secondary:
            config["models"].append(secondary)
            
            # Calculate weights based on relative performance
            primary_score = scores[primary]["composite_score"]
            secondary_score = scores[secondary]["composite_score"]
            
            total_score = primary_score + secondary_score
            primary_weight = primary_score / total_score * 0.8  # Primary gets 80% max
            secondary_weight = 1.0 - primary_weight
            
            config["weights"] = [primary_weight, secondary_weight]
            config["agreement_threshold"] = 0.75
            
        return config
        
    async def update_performance_metrics(self, 
                                       model_name: str, 
                                       investigation_result: Dict[str, Any],
                                       user_feedback: Optional[Dict[str, Any]] = None):
        """Update performance metrics based on investigation results"""
        
        timestamp = datetime.now()
        
        # Extract performance metrics
        metrics = {
            "timestamp": timestamp,
            "accuracy": investigation_result.get("confidence_score", 0.85),
            "response_time": investigation_result.get("processing_time", 60),
            "cost": investigation_result.get("execution_cost", 0.01),
            "success": 1.0 if investigation_result.get("status") == "completed" else 0.0,
            "investigation_type": investigation_result.get("investigation_type", "general"),
            "complexity": investigation_result.get("complexity_score", 0.5)
        }
        
        # Add user feedback if available
        if user_feedback:
            metrics.update({
                "user_satisfaction": user_feedback.get("satisfaction_score", 0.8),
                "result_quality": user_feedback.get("quality_rating", 0.8),
                "usefulness": user_feedback.get("usefulness_rating", 0.8)
            })
            
        # Store metrics
        self.performance_history[model_name].append(metrics)
        
        # Cleanup old metrics (keep only recent data)
        cutoff_time = timestamp - timedelta(days=30)
        self.performance_history[model_name] = [
            m for m in self.performance_history[model_name]
            if m.get("timestamp", timestamp) >= cutoff_time
        ]
        
        # Trigger optimization if performance degradation detected
        await self._check_performance_degradation(model_name, metrics)
        
    async def _check_performance_degradation(self, model_name: str, latest_metrics: Dict[str, Any]):
        """Check for performance degradation and trigger optimization"""
        
        recent_metrics = self.performance_history[model_name][-10:]  # Last 10 investigations
        
        if len(recent_metrics) < 5:
            return  # Not enough data
            
        # Calculate recent averages
        recent_accuracy = statistics.mean([m.get("accuracy", 0.85) for m in recent_metrics])
        recent_response_time = statistics.mean([m.get("response_time", 60) for m in recent_metrics])
        recent_cost = statistics.mean([m.get("cost", 0.01) for m in recent_metrics])
        
        # Compare with historical averages
        all_metrics = self.performance_history[model_name]
        if len(all_metrics) < 20:
            return  # Not enough historical data
            
        historical_accuracy = statistics.mean([m.get("accuracy", 0.85) for m in all_metrics[:-10]])
        historical_response_time = statistics.mean([m.get("response_time", 60) for m in all_metrics[:-10]])
        historical_cost = statistics.mean([m.get("cost", 0.01) for m in all_metrics[:-10]])
        
        # Check for degradation
        thresholds = self.optimization_rules["model_switching_thresholds"]
        
        degradation_detected = False
        degradation_reasons = []
        
        if recent_accuracy < historical_accuracy * (1 - thresholds["accuracy_drop"]):
            degradation_detected = True
            degradation_reasons.append("accuracy_degradation")
            
        if recent_response_time > historical_response_time * (1 + thresholds["response_time_increase"]):
            degradation_detected = True
            degradation_reasons.append("response_time_degradation")
            
        if recent_cost > historical_cost * (1 + thresholds["cost_increase"]):
            degradation_detected = True
            degradation_reasons.append("cost_increase")
            
        if degradation_detected:
            logging.warning(f"Performance degradation detected for {model_name}: {degradation_reasons}")
            await self._trigger_optimization_alert(model_name, degradation_reasons, {
                "recent_accuracy": recent_accuracy,
                "historical_accuracy": historical_accuracy,
                "recent_response_time": recent_response_time,
                "historical_response_time": historical_response_time,
                "recent_cost": recent_cost,
                "historical_cost": historical_cost
            })
            
    async def get_optimization_recommendations(self, 
                                             investigation_type: str,
                                             performance_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Get optimization recommendations for specific investigation type"""
        
        # Analyze current performance for investigation type
        type_performance = await self._analyze_type_specific_performance(investigation_type)
        
        # Identify optimization opportunities
        opportunities = await self._identify_optimization_opportunities(
            investigation_type, type_performance, performance_requirements
        )
        
        # Generate specific recommendations
        recommendations = await self._generate_specific_recommendations(
            investigation_type, opportunities, type_performance
        )
        
        return {
            "investigation_type": investigation_type,
            "current_performance": type_performance,
            "optimization_opportunities": opportunities,
            "recommendations": recommendations,
            "expected_improvements": self._calculate_expected_improvements(recommendations),
            "implementation_priority": self._prioritize_recommendations(recommendations)
        }
        
    # Helper methods for calculations and analysis
    def _get_default_metrics(self, model_name: str) -> Dict[str, Any]:
        """Get default metrics for new models"""
        # Default values based on model tier
        defaults = {
            "gpt-4-turbo": {"avg_accuracy": 0.95, "avg_response_time": 45, "avg_cost": 0.030},
            "claude-3-5-sonnet": {"avg_accuracy": 0.94, "avg_response_time": 40, "avg_cost": 0.015},
            "llama-3.1-405b": {"avg_accuracy": 0.88, "avg_response_time": 35, "avg_cost": 0.005},
            "mixtral-8x22b": {"avg_accuracy": 0.86, "avg_response_time": 30, "avg_cost": 0.006},
        }
        
        return defaults.get(model_name, {
            "avg_accuracy": 0.85,
            "avg_response_time": 60,
            "avg_cost": 0.01,
            "success_rate": 0.95,
            "reliability_score": 0.85
        })
        
    def _calculate_specialization_match(self, model_name: str, investigation_type: str) -> float:
        """Calculate how well a model matches investigation type specialization"""
        
        specialization_matrix = {
            "gpt-4-turbo": {"legal": 0.95, "technical": 0.90, "general": 0.85},
            "claude-3-5-sonnet": {"document": 0.95, "ethical": 0.90, "analysis": 0.88},
            "llama-3.1-405b": {"technical": 0.88, "general": 0.85, "pattern": 0.82},
            "mixtral-8x22b": {"multilingual": 0.90, "code": 0.85, "structured": 0.83}
        }
        
        model_specs = specialization_matrix.get(model_name, {})
        return model_specs.get(investigation_type, 0.75)  # Default match score
        
    def _calculate_recommendation_confidence(self, performance_data: Dict[str, Any]) -> float:
        """Calculate confidence in recommendation based on data quality"""
        
        sample_size = performance_data.get("sample_size", 0)
        accuracy_std = performance_data.get("accuracy_std", 0.1)
        success_rate = performance_data.get("success_rate", 0.95)
        
        # Confidence based on sample size
        size_confidence = min(sample_size / 50, 1.0)  # Full confidence at 50+ samples
        
        # Confidence based on consistency (lower std = higher confidence)
        consistency_confidence = max(0, 1 - (accuracy_std / 0.2))  # 0.2 std = 0 confidence
        
        # Confidence based on success rate
        success_confidence = success_rate
        
        # Combined confidence
        return (size_confidence * 0.4 + consistency_confidence * 0.3 + success_confidence * 0.3)

# Export the optimizer class
__all__ = ['ModelPerformanceOptimizer', 'ModelPerformanceMetrics', 'OptimizationTarget']

