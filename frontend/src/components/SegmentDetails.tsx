import type { ProductionSegment } from "../types/Production";

interface SegmentDetailsProps {
    readonly segment: ProductionSegment | null;
}

export default function SegmentDetails({
    segment,
}: SegmentDetailsProps) {

if (!segment) {
    return (
        <div>
            No segment selected.
        </div>
    );
}

return (

    <div>

        <h3>Segment Details</h3>

        <p><strong>Segment ID:</strong> {segment.segmentId}</p>

        <p><strong>Production ID:</strong> {segment.prodId}</p>

        <p><strong>Start:</strong> {segment.startTime.toLocaleString()}</p>

        <p><strong>Stop:</strong> {segment.stopTime.toLocaleString()}</p>

        <p><strong>Runtime:</strong> {segment.runTime} s</p>

        <p><strong>Mass:</strong> {segment.massTotal} t</p>

    </div>

);
}