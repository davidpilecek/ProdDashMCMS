import { Box, Divider, Typography } from "@mui/material";

import type { ProductionUnit } from "../types/Production";

interface ProductionUnitDetailsProps {
    readonly productionUnit: ProductionUnit | null;
}

function formatRuntime(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const remainingSeconds = Math.floor(seconds % 60);

    return `${hours} h ${minutes} min ${remainingSeconds} s`;
}

export default function ProductionUnitDetails({
    productionUnit,
}: ProductionUnitDetailsProps) {
    if (!productionUnit) {
        return null;
    }

    const { statistics } = productionUnit;

    return (
        <Box sx={{padding:4}}>
            <Typography variant="h6">Production Unit</Typography>

            <Box sx={{ mt: 2}}>
                {/* <Typography variant="subtitle2">
                    Identification
                </Typography> */}

                <Box>
                    <strong>Production ID</strong>
                    <div>{productionUnit.prodId}</div>
                </Box>

                <Box>
                    <strong>Production Number</strong>
                    <div>{productionUnit.prodNum}</div>
                </Box>

                <Box>
                    <strong>Description</strong>
                    <div>{productionUnit.prodDesc}</div>
                </Box>

                <Box>
                    <strong>Recipe</strong>
                    <div>{productionUnit.recipeName}</div>
                </Box>
            </Box>

            <Divider />

            {/* <Typography variant="subtitle2">
                Production Statistics
            </Typography> */}

            <Box
                sx={{
                    display: "grid",
                    gridTemplateColumns: "1fr 1fr",
                    gap: 2,
                }}
            >
                <Box>
                    <strong>Segments</strong>
                    <div>{statistics.segmentCount}</div>
                </Box>

                <Box>
                    <strong>Runtime</strong>
                    <div>
                        {formatRuntime(statistics.runTime)}
                    </div>
                </Box>

                <Box>
                    <strong>Mass</strong>
                    <div>
                        {statistics.mass.toFixed(2)} t
                    </div>
                </Box>

                <Box>
                    <strong>Rate</strong>
                    <div>
                        {statistics.rate.toFixed(2)} t/h
                    </div>
                </Box>

                <Box>
                    <strong>Total incl. additives</strong>
                    <div>
                        {statistics.totalInclAdditives.toFixed(2)} t
                    </div>
                </Box>
            </Box>

            <Divider />

            {/* <Typography variant="subtitle2">
                Additives
            </Typography> */}

            <Box
                sx={{
                    display: "grid",
                    gridTemplateColumns:
                        "1fr 1fr 1fr",
                    columnGap: 2,
                    rowGap: 1,
                }}
            >
                <strong>Additive</strong>
                <strong>Mass</strong>
                <strong>Percentage</strong>

                <span>Additive 1</span>
                <span>
                    {statistics.additives.add1.mass.toFixed(2)} t
                </span>
                <span>
                    {statistics.additives.add1.percent.toFixed(2)} %
                </span>

                <span>Additive 2</span>
                <span>
                    {statistics.additives.add2.mass.toFixed(2)} t
                </span>
                <span>
                    {statistics.additives.add2.percent.toFixed(2)} %
                </span>

                <span>Additive 3</span>
                <span>
                    {statistics.additives.add3.mass.toFixed(2)} t
                </span>
                <span>
                    {statistics.additives.add3.percent.toFixed(2)} %
                </span>

                <span>Additive 4</span>
                <span>
                    {statistics.additives.add4.mass.toFixed(2)} t
                </span>
                <span>
                    {statistics.additives.add4.percent.toFixed(2)} %
                </span>

                <span>Additive 5</span>
                <span>
                    {statistics.additives.add5.mass.toFixed(2)} t
                </span>
                <span>
                    {statistics.additives.add5.percent.toFixed(2)} %
                </span>
            </Box>
        </Box>
    );
}