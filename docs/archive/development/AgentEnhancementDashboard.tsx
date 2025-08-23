import React, { useState, useEffect, useMemo } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, Area, AreaChart,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar,
  TreeMap, Treemap
} from 'recharts';

// Enhanced data types based on agentgen project analysis
interface AgentTransformation {
  agentName: string;
  category: 'core' | 'development' | 'infrastructure' | 'specialist' | 'business' | 'security' | 'quality-testing';
  complexity: 'Green' | 'Yellow' | 'Red';
  beforeTokens: number;
  afterTokens: number;
  knowledgePoints: number;
  domainAccuracy: number;
  performanceMs: number;
  enhancementPattern: 'Weak→Strong' | 'General→Specialist' | 'Simple→Sophisticated';
  profile: string[];
  capabilities: string[];
}

interface ProfileData {
  name: string;
  agents: number;
  focus: string;
  teamSize: string;
  primaryUse: string;
  complexity: number;
}

// Sample data based on agentgen project structure
const transformationData: AgentTransformation[] = [
  {
    agentName: 'react-specialist',
    category: 'specialist',
    complexity: 'Yellow',
    beforeTokens: 800,
    afterTokens: 3200,
    knowledgePoints: 850,
    domainAccuracy: 97,
    performanceMs: 420,
    enhancementPattern: 'General→Specialist',
    profile: ['modern-web-stack', 'development-team'],
    capabilities: ['React Hooks', 'Performance Optimization', 'Testing', 'SSR/SSG']
  },
  {
    agentName: 'architect-specialist',
    category: 'specialist',
    complexity: 'Red',
    beforeTokens: 1200,
    afterTokens: 8500,
    knowledgePoints: 1200,
    domainAccuracy: 99,
    performanceMs: 480,
    enhancementPattern: 'Simple→Sophisticated',
    profile: ['enterprise-leadership', 'development-team'],
    capabilities: ['System Design', 'Microservices', 'Scalability', 'Performance']
  },
  {
    agentName: 'debugger',
    category: 'quality-testing',
    complexity: 'Yellow',
    beforeTokens: 600,
    afterTokens: 2400,
    knowledgePoints: 750,
    domainAccuracy: 94,
    performanceMs: 380,
    enhancementPattern: 'Weak→Strong',
    profile: ['startup-mvp', 'development-team'],
    capabilities: ['Root Cause Analysis', 'Testing', 'Error Handling', 'Monitoring']
  },
  {
    agentName: 'security-auditor',
    category: 'security',
    complexity: 'Red',
    beforeTokens: 900,
    afterTokens: 6800,
    knowledgePoints: 980,
    domainAccuracy: 98,
    performanceMs: 450,
    enhancementPattern: 'General→Specialist',
    profile: ['enterprise-leadership'],
    capabilities: ['Threat Modeling', 'Vulnerability Assessment', 'Compliance', 'Penetration Testing']
  },
  {
    agentName: 'frontend-developer',
    category: 'development',
    complexity: 'Yellow',
    beforeTokens: 700,
    afterTokens: 2800,
    knowledgePoints: 720,
    domainAccuracy: 92,
    performanceMs: 340,
    enhancementPattern: 'Weak→Strong',
    profile: ['modern-web-stack', 'startup-mvp'],
    capabilities: ['UI/UX', 'Responsive Design', 'Accessibility', 'Performance']
  }
];

const profilesData: ProfileData[] = [
  { name: 'enterprise-leadership', agents: 9, focus: 'Strategic Decision-Making', teamSize: '50+ people', primaryUse: 'Architecture & Strategy', complexity: 0.9 },
  { name: 'modern-web-stack', agents: 12, focus: 'TypeScript/React Excellence', teamSize: '15-50 people', primaryUse: 'Modern Web Apps', complexity: 0.7 },
  { name: 'startup-mvp', agents: 11, focus: 'Rapid Development', teamSize: '5-15 people', primaryUse: 'MVP & Prototypes', complexity: 0.6 },
  { name: 'development-team', agents: 18, focus: 'Complete Workflow', teamSize: 'Any size', primaryUse: 'Full Development', complexity: 0.8 },
  { name: 'core', agents: 15, focus: 'Essential Agents', teamSize: 'Any size', primaryUse: 'Foundation', complexity: 0.5 }
];

// Color schemes
const complexityColors = {
  Green: '#10B981',
  Yellow: '#F59E0B', 
  Red: '#EF4444'
};

const categoryColors = {
  'core': '#6B7280',
  'development': '#3B82F6',
  'infrastructure': '#8B5CF6',
  'specialist': '#F59E0B',
  'business': '#10B981',
  'security': '#EF4444',
  'quality-testing': '#EC4899'
};

const AgentEnhancementDashboard: React.FC = () => {
  const [selectedMetric, setSelectedMetric] = useState<'tokens' | 'knowledge' | 'performance'>('tokens');
  const [selectedProfile, setSelectedProfile] = useState<string>('all');
  const [animationClass, setAnimationClass] = useState('');

  // Filtered data based on selected profile
  const filteredData = useMemo(() => {
    if (selectedProfile === 'all') return transformationData;
    return transformationData.filter(agent => agent.profile.includes(selectedProfile));
  }, [selectedProfile]);

  // Metrics calculation
  const metrics = useMemo(() => {
    const totalBefore = filteredData.reduce((sum, agent) => sum + agent.beforeTokens, 0);
    const totalAfter = filteredData.reduce((sum, agent) => sum + agent.afterTokens, 0);
    const avgAccuracy = filteredData.reduce((sum, agent) => sum + agent.domainAccuracy, 0) / filteredData.length;
    const avgPerformance = filteredData.reduce((sum, agent) => sum + agent.performanceMs, 0) / filteredData.length;
    
    return {
      tokenIncrease: ((totalAfter - totalBefore) / totalBefore * 100).toFixed(1),
      avgAccuracy: avgAccuracy.toFixed(1),
      avgPerformance: avgPerformance.toFixed(0),
      totalAgents: filteredData.length
    };
  }, [filteredData]);

  // Chart data transformations
  const enhancementChartData = filteredData.map(agent => ({
    name: agent.agentName,
    before: agent.beforeTokens,
    after: agent.afterTokens,
    increase: agent.afterTokens - agent.beforeTokens,
    category: agent.category,
    complexity: agent.complexity
  }));

  const categoryDistribution = Object.entries(
    filteredData.reduce((acc, agent) => {
      acc[agent.category] = (acc[agent.category] || 0) + 1;
      return acc;
    }, {} as Record<string, number>)
  ).map(([category, count]) => ({
    name: category,
    value: count,
    color: categoryColors[category as keyof typeof categoryColors]
  }));

  const performanceData = filteredData.map(agent => ({
    name: agent.agentName,
    accuracy: agent.domainAccuracy,
    performance: 1000 - agent.performanceMs, // Invert for better visualization
    knowledge: agent.knowledgePoints / 10,
    complexity: agent.complexity === 'Red' ? 3 : agent.complexity === 'Yellow' ? 2 : 1
  }));

  // Animation trigger
  useEffect(() => {
    setAnimationClass('animate-in');
    const timer = setTimeout(() => setAnimationClass(''), 500);
    return () => clearTimeout(timer);
  }, [selectedProfile]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🤖 Agent Enhancement Transformation Dashboard
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Visualizing the evolution from token reduction to capability enhancement in the agentgen system. 
            Track knowledge amplification, performance metrics, and strategic profile impact.
          </p>
        </div>

        {/* Controls */}
        <div className="flex flex-wrap gap-4 items-center justify-center bg-white p-4 rounded-lg shadow-sm">
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-gray-700">Profile:</label>
            <select 
              value={selectedProfile}
              onChange={(e) => setSelectedProfile(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Profiles</option>
              {profilesData.map(profile => (
                <option key={profile.name} value={profile.name}>
                  {profile.name} ({profile.agents} agents)
                </option>
              ))}
            </select>
          </div>
          
          <div className="flex items-center gap-2">
            <label className="text-sm font-medium text-gray-700">Metric:</label>
            <div className="flex gap-1">
              {(['tokens', 'knowledge', 'performance'] as const).map(metric => (
                <button
                  key={metric}
                  onClick={() => setSelectedMetric(metric)}
                  className={`px-3 py-2 text-sm rounded-md transition-colors ${
                    selectedMetric === metric 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {metric.charAt(0).toUpperCase() + metric.slice(1)}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className={`grid grid-cols-1 md:grid-cols-4 gap-4 ${animationClass}`}>
          {[
            { label: 'Token Increase', value: `+${metrics.tokenIncrease}%`, color: 'text-green-600', bg: 'bg-green-50' },
            { label: 'Avg Domain Accuracy', value: `${metrics.avgAccuracy}%`, color: 'text-blue-600', bg: 'bg-blue-50' },
            { label: 'Avg Performance', value: `${metrics.avgPerformance}ms`, color: 'text-purple-600', bg: 'bg-purple-50' },
            { label: 'Enhanced Agents', value: metrics.totalAgents.toString(), color: 'text-orange-600', bg: 'bg-orange-50' }
          ].map((metric, index) => (
            <div key={metric.label} className={`${metric.bg} p-6 rounded-lg border border-gray-200`}>
              <h3 className="text-sm font-medium text-gray-700 mb-1">{metric.label}</h3>
              <p className={`text-2xl font-bold ${metric.color}`}>{metric.value}</p>
            </div>
          ))}
        </div>

        {/* Main Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Token Enhancement Chart */}
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Token Enhancement by Agent</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={enhancementChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => [
                    `${value} tokens`, 
                    name === 'before' ? 'Before Enhancement' : 'After Enhancement'
                  ]}
                />
                <Legend />
                <Bar dataKey="before" fill="#94A3B8" name="Before" />
                <Bar dataKey="after" fill="#3B82F6" name="After" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Category Distribution */}
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Agent Category Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryDistribution}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  dataKey="value"
                  label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                >
                  {categoryDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Performance Radar Chart */}
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Multi-Dimensional Performance Analysis</h3>
          <ResponsiveContainer width="100%" height={400}>
            <RadarChart data={performanceData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="name" />
              <PolarRadiusAxis angle={90} domain={[0, 100]} />
              <Radar 
                name="Domain Accuracy" 
                dataKey="accuracy" 
                stroke="#3B82F6" 
                fill="#3B82F6" 
                fillOpacity={0.1}
              />
              <Radar 
                name="Performance Score" 
                dataKey="performance" 
                stroke="#10B981" 
                fill="#10B981" 
                fillOpacity={0.1}
              />
              <Radar 
                name="Knowledge Points" 
                dataKey="knowledge" 
                stroke="#F59E0B" 
                fill="#F59E0B" 
                fillOpacity={0.1}
              />
              <Legend />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Profile Analysis */}
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Strategic Profile Analysis</h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={profilesData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => [
                  name === 'agents' ? `${value} agents` : 
                  name === 'complexity' ? `${(value as number * 100).toFixed(0)}% complexity` : value,
                  name === 'agents' ? 'Agent Count' : 'Complexity Level'
                ]}
              />
              <Area 
                type="monotone" 
                dataKey="agents" 
                stackId="1" 
                stroke="#3B82F6" 
                fill="#3B82F6" 
                fillOpacity={0.8}
              />
              <Area 
                type="monotone" 
                dataKey="complexity" 
                stackId="2" 
                stroke="#F59E0B" 
                fill="#F59E0B" 
                fillOpacity={0.6}
                yAxisId="right"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Enhancement Patterns */}
        <div className="bg-white p-6 rounded-lg shadow-sm">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Enhancement Pattern Analysis</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {['Weak→Strong', 'General→Specialist', 'Simple→Sophisticated'].map(pattern => {
              const count = filteredData.filter(agent => agent.enhancementPattern === pattern).length;
              const percentage = (count / filteredData.length * 100).toFixed(1);
              
              return (
                <div key={pattern} className="p-4 border border-gray-200 rounded-lg">
                  <h4 className="font-medium text-gray-900 mb-2">{pattern}</h4>
                  <p className="text-2xl font-bold text-blue-600">{count}</p>
                  <p className="text-sm text-gray-600">{percentage}% of agents</p>
                </div>
              );
            })}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-sm text-gray-500 bg-white p-4 rounded-lg">
          <p>
            🚀 Agent Enhancement System | Philosophy: Token Reduction → Capability Enhancement | 
            Performance: &lt;500ms queries, &gt;95% accuracy, 30%+ velocity improvement
          </p>
        </div>
      </div>

      <style jsx>{`
        .animate-in {
          animation: slideInUp 0.5s ease-out;
        }
        
        @keyframes slideInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default AgentEnhancementDashboard;