import type { ProductionUnit } from "../types/Production";

interface ProductionUnitDetailsProps {
    readonly productionUnit: ProductionUnit | null;
}

export default function ProductionUnitDetails({
    productionUnit,
}: ProductionUnitDetailsProps) {

    if (!productionUnit) {
        return (
            <div>
                No production unit selected.
            </div>
        );
    }

    return (
        <div>
            <h3>Production Unit</h3>

            <p>
                <strong>Production ID:</strong>{" "}
                {productionUnit.prodId}
            </p>

            <p>
                <strong>Production Number:</strong>{" "}
                {productionUnit.prodNum}
            </p>

            <p>
                <strong>Description:</strong>{" "}
                {productionUnit.prodDesc}
            </p>

            <p>
                <strong>Recipe:</strong>{" "}
                {productionUnit.recipeName}
            </p>
        </div>
    );
}