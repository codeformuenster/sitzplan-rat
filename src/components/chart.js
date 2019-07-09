import React from 'react'
import {
    ResponsiveContainer, PieChart, Pie, Cell, Tooltip
} from 'recharts';

const PARTYCOLORS = {
    gruene: 'green',
    spd: 'red',
    linke: 'red',
    cdu: 'black',
    piraten: 'orange',
    afd: 'blue',
    fdp: 'yellow'
}

const RADIAN = Math.PI / 180;
const renderCustomizedLabel = ({
    x, y, name, ...props
}) => {

    return (
        <text x={x} y={y} fill={'black'}>
            {name}
        </text>
    );
};

const Chart = ({ parties, chartOnClick }) => {

    return <ResponsiveContainer>
        <PieChart>
            <Pie
                data={parties}
                dataKey="value"
                fill="#8884d8"
                labelLine={false}
                label={renderCustomizedLabel}
                innerRadius={'50%'}
                onClick={(e) => (chartOnClick(e))}>

                {
                    parties.map((entry, index) => <Cell key={`cell-${index}`} fill={PARTYCOLORS[entry.name]} />)
                }
            </Pie>
            <Tooltip />
        </PieChart>
    </ResponsiveContainer>
}

export default Chart;