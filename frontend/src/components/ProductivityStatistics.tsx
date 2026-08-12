import type { ProductionStatistics } from "../types/Production";

interface ProductivityStatisticsProps {
    readonly statistics: ProductionStatistics | null;
}

export default function ProductivityStatistics({
    statistics,
}: ProductivityStatisticsProps) {
    if (!statistics) {
        return null;
    }

    return (
        <div>
            <h3>Statistics</h3>

            <table>
    <thead>
        <tr>
            <th>Metric</th>
            <th>Segment</th>
            <th>Day</th>
            <th>Month</th>
        </tr>
    </thead>

    <tbody>
        <tr>
            <td>Tonnes</td>
            <td>{statistics.segment.tonnes.toFixed(2)} t</td>
            <td>{statistics.day.tonnes.toFixed(2)} t</td>
            <td>{statistics.month.tonnes.toFixed(2)} t</td>
        </tr>

        <tr>
            <td>Hours</td>
            <td>{statistics.segment.hours.toFixed(2)} h</td>
            <td>{statistics.day.hours.toFixed(2)} h</td>
            <td>{statistics.month.hours.toFixed(2)} h</td>
        </tr>

        <tr>
            <td>Average Rate</td>
            <td>{statistics.segment.rate.toFixed(2)} t/h</td>
            <td>{statistics.day.rate.toFixed(2)} t/h</td>
            <td>{statistics.month.rate.toFixed(2)} t/h</td>
        </tr>
    </tbody>
</table>
        </div>
    );
}

