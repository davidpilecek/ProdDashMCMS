import type {
	DashboardMonth,
	OverviewMetric,
	ProductionGraphPoint,
	ReportAction,
} from '../types/Production';

export const dashboardMonths: DashboardMonth[] = [
	{ value: '2026-01', label: 'January 2026' },
	{ value: '2026-02', label: 'February 2026' },
	{ value: '2026-03', label: 'March 2026' },
	{ value: '2026-04', label: 'April 2026' },
];

export const overviewMetrics: OverviewMetric[] = [
	{
		label: 'Output',
		value: '18.4 kt',
		trend: '+4.8% vs previous month',
		note: 'Historical production volume for the selected month.',
		tone: 'positive',
	},
	{
		label: 'Availability',
		value: '96.2%',
		trend: '+0.6 percentage points',
		note: 'Share of planned runtime captured in the overview.',
		tone: 'positive',
	},
	{
		label: 'Scrap rate',
		value: '2.1%',
		trend: '-0.3 percentage points',
		note: 'Placeholder statistic until the backend model is connected.',
		tone: 'neutral',
	},
	{
		label: 'Open batches',
		value: '6',
		trend: '2 require review',
		note: 'Counts shown here are driven by mock data for phase 1.',
		tone: 'warning',
	},
];

export const productionGraphPoints: ProductionGraphPoint[] = [
	{ label: 'W1', actual: 74, target: 88 },
	{ label: 'W2', actual: 81, target: 88 },
	{ label: 'W3', actual: 86, target: 88 },
	{ label: 'W4', actual: 91, target: 88 },
	{ label: 'W5', actual: 89, target: 88 },
	{ label: 'W6', actual: 93, target: 88 },
	{ label: 'W7', actual: 87, target: 88 },
	{ label: 'W8', actual: 95, target: 88 },
	{ label: 'W9', actual: 92, target: 88 },
	{ label: 'W10', actual: 90, target: 88 },
	{ label: 'W11', actual: 94, target: 88 },
	{ label: 'W12', actual: 97, target: 88 },
];


export const reportActions: ReportAction[] = [
	{
		label: 'Generate monthly report',
		description: 'Creates a PDF summary once the backend report service is available.',
	},
	{
		label: 'Export batch list',
		description: 'Exports the current batch table view as a spreadsheet placeholder.',
	},
	{
		label: 'Share overview snapshot',
		description: 'Prepares a read-only dashboard snapshot for review.',
	},
];
