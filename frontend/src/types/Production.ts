export interface DashboardMonth {
	value: string;
	label: string;
}

export interface OverviewMetric {
	label: string;
	value: string;
	trend: string;
	note: string;
	tone: 'positive' | 'neutral' | 'warning';
}

export interface ProductionGraphPoint {
	label: string;
	actual: number;
	target: number;
}

export interface ProductionSegment {
    readonly segmentId: string;
    readonly prodId: string;
    readonly usrId: string;

    readonly startTime: Date;
    readonly stopTime: Date;
    readonly runTime: number;

    readonly massTotal: number;

    readonly add1Total: number;
    readonly add2Total: number;
    readonly add3Total: number;
    readonly add4Total: number;
    readonly add5Total: number;

    readonly totalInclAdditives: number;

    readonly add1Percent: number;
    readonly add2Percent: number;
    readonly add3Percent: number;
    readonly add4Percent: number;
    readonly add5Percent: number;
}

export interface ProductionUnit {
    readonly prodId: string;
    readonly prodNum: string;
    readonly prodDesc: string;
    readonly recipeName: string;
}

export interface ReportAction {
	label: string;
	description: string;
}

export interface ProductionMonth {
    readonly month: number;
    readonly year: number;

    readonly segments: ProductionSegment[];
    readonly productionUnits: ProductionUnit[];

}

export interface ProductionStatistics {
    readonly segment: ProductionStats;
    readonly day: ProductionStats;
    readonly month: ProductionStats;
}

export interface ProductionStats {
    readonly tonnes: number;
    readonly hours: number;
    readonly rate: number;
}