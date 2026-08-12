import type {
    ProductionMonth,
    ProductionSegment,
    ProductionStatistics,
} from "../types/Production";

const API_BASE_URL = "http://127.0.0.1:5000";

interface ProductionSegmentResponse
    extends Omit<ProductionSegment, "startTime" | "stopTime"> {
    startTime: string;
    stopTime: string;
}

export async function getProductionMonth(
    month: number,
    year: number,
): Promise<ProductionMonth> {

    const response = await fetch(
        `${API_BASE_URL}/api/production?month=${month}&year=${year}`,
    );

    if (!response.ok) {
        throw new Error(
            `Failed to load production data: ${response.status}`,
        );
    }

    const data: {
        month: number;
        year: number;
        segments: ProductionSegmentResponse[];
        productionUnits: ProductionMonth["productionUnits"];
    } = await response.json();

    return {
        month: data.month,
        year: data.year,

        segments: data.segments.map(
            (segment): ProductionSegment => ({
                ...segment,
                startTime: new Date(segment.startTime),
                stopTime: new Date(segment.stopTime),
            }),
        ),

        productionUnits: data.productionUnits,
    };
}

export async function getProductionStatistics(
    month: number,
    year: number,
    segmentId: string,
): Promise<ProductionStatistics> {

    const response = await fetch(
        `${API_BASE_URL}/api/production/statistics` +
        `?month=${month}` +
        `&year=${year}` +
        `&segmentId=${encodeURIComponent(segmentId)}`,
    );

    if (!response.ok) {
        throw new Error(
            `Failed to load production statistics: ${response.status}`,
        );
    }

    return response.json();
}