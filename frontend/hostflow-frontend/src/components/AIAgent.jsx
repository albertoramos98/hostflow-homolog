import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { 
  Brain, 
  TrendingUp, 
  AlertTriangle, 
  Target, 
  BarChart3,
  Users,
  DollarSign,
  Calendar,
  Lightbulb,
  Activity,
  Zap
} from 'lucide-react'

export default function AIAgent() {
  const [agentInfo, setAgentInfo] = useState(null)
  const [dailyBriefing, setDailyBriefing] = useState(null)
  const [insights, setInsights] = useState([])
  const [predictions, setPredictions] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAgentData()
  }, [])

  const loadAgentData = async () => {
    try {
      setLoading(true)
      
      // Carregar informações do agente
      const agentResponse = await fetch('/api/agent/info')
      const agentData = await agentResponse.json()
      setAgentInfo(agentData)

      // Carregar briefing diário
      const briefingResponse = await fetch('/api/agent/briefing/daily')
      const briefingData = await briefingResponse.json()
      setDailyBriefing(briefingData)

      // Carregar insights
      const insightsResponse = await fetch('/api/agent/insights')
      const insightsData = await insightsResponse.json()
      setInsights(insightsData)

      // Carregar previsões
      const predictionsResponse = await fetch('/api/agent/predictions')
      const predictionsData = await predictionsResponse.json()
      setPredictions(predictionsData)

    } catch (error) {
      console.error('Erro ao carregar dados do agente:', error)
    } finally {
      setLoading(false)
    }
  }

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'destructive'
      case 'medium': return 'default'
      case 'low': return 'secondary'
      default: return 'default'
    }
  }

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high': return <AlertTriangle className="h-4 w-4" />
      case 'medium': return <Target className="h-4 w-4" />
      case 'low': return <Activity className="h-4 w-4" />
      default: return <Activity className="h-4 w-4" />
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <div className="bg-blue-100 p-3 rounded-full">
            <Brain className="h-8 w-8 text-blue-600 animate-pulse" />
          </div>
          <div>
            <h2 className="text-3xl font-bold text-gray-900">Agente de IA</h2>
            <p className="text-gray-600">Carregando análises...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header do Agente */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="bg-blue-100 p-3 rounded-full">
            <Brain className="h-8 w-8 text-blue-600" />
          </div>
          <div>
            <h2 className="text-3xl font-bold text-gray-900">
              {agentInfo?.name || 'InsightAI'}
            </h2>
            <p className="text-gray-600">Agente de Insights e Análises Preditivas</p>
          </div>
        </div>
        <Button onClick={loadAgentData} className="bg-blue-500 hover:bg-blue-600">
          <Zap className="h-4 w-4 mr-2" />
          Atualizar Análises
        </Button>
      </div>

      {/* Informações do Agente */}
      {agentInfo && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Brain className="h-5 w-5" />
              <span>Informações do Agente</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Personalidade</h4>
                <p className="text-sm text-gray-600">{agentInfo.personality}</p>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Status</h4>
                <Badge variant="default" className="bg-green-100 text-green-800">
                  {agentInfo.status}
                </Badge>
              </div>
            </div>
            <div className="mt-4">
              <h4 className="font-semibold text-gray-900 mb-2">Capacidades</h4>
              <div className="flex flex-wrap gap-2">
                {agentInfo.capabilities?.map((capability, index) => (
                  <Badge key={index} variant="outline">
                    {capability}
                  </Badge>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Briefing Diário */}
      {dailyBriefing && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Calendar className="h-5 w-5" />
              <span>Briefing Diário</span>
            </CardTitle>
            <CardDescription>
              {dailyBriefing.date} - {dailyBriefing.summary}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {dailyBriefing.performance_snapshot?.revenue_trend}
                </div>
                <div className="text-sm text-gray-600">Receita</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {dailyBriefing.performance_snapshot?.occupancy_rate}
                </div>
                <div className="text-sm text-gray-600">Ocupação</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {dailyBriefing.performance_snapshot?.customer_satisfaction}
                </div>
                <div className="text-sm text-gray-600">Satisfação</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {dailyBriefing.performance_snapshot?.marketing_roi}
                </div>
                <div className="text-sm text-gray-600">ROI Marketing</div>
              </div>
            </div>

            <div>
              <h4 className="font-semibold text-gray-900 mb-3">Alertas Principais</h4>
              <div className="space-y-2">
                {dailyBriefing.key_alerts?.map((alert, index) => (
                  <div key={index} className="flex items-center space-x-2 p-2 bg-yellow-50 rounded-lg">
                    <AlertTriangle className="h-4 w-4 text-yellow-600" />
                    <span className="text-sm text-gray-700">{alert}</span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Tabs para diferentes análises */}
      <Tabs defaultValue="insights" className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="insights">Insights Acionáveis</TabsTrigger>
          <TabsTrigger value="predictions">Previsões</TabsTrigger>
          <TabsTrigger value="actions">Ações Prioritárias</TabsTrigger>
        </TabsList>

        <TabsContent value="insights" className="space-y-4">
          <div className="grid gap-4">
            {insights.map((insight, index) => (
              <Card key={index}>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center space-x-2">
                      <Lightbulb className="h-5 w-5" />
                      <span>{insight.title}</span>
                    </CardTitle>
                    <Badge variant={getPriorityColor(insight.priority)} className="flex items-center space-x-1">
                      {getPriorityIcon(insight.priority)}
                      <span>{insight.priority}</span>
                    </Badge>
                  </div>
                  <CardDescription>{insight.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div>
                      <h5 className="font-semibold text-gray-900">Ação Recomendada:</h5>
                      <p className="text-sm text-gray-600">{insight.action}</p>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <h5 className="font-semibold text-gray-900">Impacto Esperado:</h5>
                        <p className="text-sm text-green-600">{insight.impact}</p>
                      </div>
                      <div>
                        <h5 className="font-semibold text-gray-900">Prazo:</h5>
                        <p className="text-sm text-gray-600">{insight.timeline}</p>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="predictions" className="space-y-4">
          {predictions && (
            <div className="grid gap-4">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <TrendingUp className="h-5 w-5" />
                    <span>Previsões de Receita</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h5 className="font-semibold text-gray-900">Próximo Mês</h5>
                      <p className="text-2xl font-bold text-green-600">
                        R$ {predictions.details?.next_month_revenue?.value?.toLocaleString('pt-BR')}
                      </p>
                      <p className="text-sm text-gray-600">
                        Confiança: {predictions.details?.next_month_revenue?.confidence}%
                      </p>
                    </div>
                    <div>
                      <h5 className="font-semibold text-gray-900">Taxa de Ocupação</h5>
                      <p className="text-2xl font-bold text-blue-600">
                        {predictions.details?.occupancy_forecast?.value?.toFixed(1)}%
                      </p>
                      <p className="text-sm text-gray-600">
                        Confiança: {predictions.details?.occupancy_forecast?.confidence}%
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Users className="h-5 w-5" />
                    <span>Análise de Conversão de Leads</span>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-xl font-bold text-green-600">
                        {predictions.details?.lead_conversion_probability?.high_probability_leads}
                      </div>
                      <div className="text-sm text-gray-600">Alta Probabilidade</div>
                    </div>
                    <div className="text-center">
                      <div className="text-xl font-bold text-yellow-600">
                        {predictions.details?.lead_conversion_probability?.medium_probability_leads}
                      </div>
                      <div className="text-sm text-gray-600">Média Probabilidade</div>
                    </div>
                    <div className="text-center">
                      <div className="text-xl font-bold text-red-600">
                        {predictions.details?.lead_conversion_probability?.low_probability_leads}
                      </div>
                      <div className="text-sm text-gray-600">Baixa Probabilidade</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        <TabsContent value="actions" className="space-y-4">
          {dailyBriefing?.priority_actions && (
            <div className="grid gap-4">
              {dailyBriefing.priority_actions.map((action, index) => (
                <Card key={index}>
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center space-x-2">
                        <Target className="h-5 w-5" />
                        <span>{action.title}</span>
                      </CardTitle>
                      <Badge variant="destructive">
                        Prioridade Alta
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 mb-3">{action.description}</p>
                    <div className="bg-blue-50 p-3 rounded-lg">
                      <h5 className="font-semibold text-blue-900 mb-1">Ação Recomendada:</h5>
                      <p className="text-blue-800 text-sm">{action.action}</p>
                    </div>
                    <div className="mt-3 flex justify-between text-sm">
                      <span className="text-green-600 font-medium">{action.impact}</span>
                      <span className="text-gray-500">{action.timeline}</span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}

