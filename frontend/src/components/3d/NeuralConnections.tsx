import React, { useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { useMetaMindStore } from '../../store/useMetaMindStore';

const Connection: React.FC<{ start: [number, number, number], end: [number, number, number], color: string, isActive: boolean }> = ({ start, end, color, isActive }) => {
  const curve = useMemo(() => {
    const v1 = new THREE.Vector3(...start);
    const v2 = new THREE.Vector3(...end);
    return new THREE.CatmullRomCurve3([
      v1,
      new THREE.Vector3((v1.x + v2.x) / 2, (v1.y + v2.y) / 2 + 1, (v1.z + v2.z) / 2),
      v2
    ]);
  }, [start, end]);

  const points = curve.getPoints(50);
  const geometry = new THREE.BufferGeometry().setFromPoints(points);
  
  const packetRef = React.useRef<THREE.Mesh>(null);
  
  useFrame((state) => {
    if (isActive && packetRef.current) {
      const time = state.clock.getElapsedTime();
      const t = (time * 0.5) % 1;
      const point = curve.getPointAt(t);
      packetRef.current.position.set(point.x, point.y, point.z);
      packetRef.current.scale.setScalar(0.1 + Math.sin(time * 10) * 0.05);
    }
  });

  return (
    <group>
      <line geometry={geometry}>
        <lineBasicMaterial attach="material" color={color} opacity={isActive ? 0.3 : 0.05} transparent linewidth={1} />
      </line>
      {isActive && (
        <mesh ref={packetRef}>
          <sphereGeometry args={[0.08, 16, 16]} />
          <meshStandardMaterial 
            color={color} 
            emissive={color} 
            emissiveIntensity={4} 
            toneMapped={false}
          />
        </mesh>
      )}
    </group>
  );
};

export const NeuralConnections: React.FC = () => {
  const { agents } = useMetaMindStore();
  
  const agentConfigs = [
    { name: "Analyst Agent", color: "#00f3ff", pos: [-6, 2, 0] },
    { name: "Architect Agent", color: "#7000ff", pos: [-2, 2, 0] },
    { name: "Engineer Agent", color: "#ff00c8", pos: [2, 2, 0] },
    { name: "Executor Agent", color: "#ff8c00", pos: [6, 2, 0] },
    { name: "Evaluator Agent", color: "#00ff00", pos: [4, -2, 0] },
    { name: "Critic Agent", color: "#ff0000", pos: [0, -2, 0] },
    { name: "Explainer Agent", color: "#ffff00", pos: [-4, -2, 0] },
  ];

  const connections = useMemo(() => {
    const pairs: any[] = [];
    for (let i = 0; i < agentConfigs.length - 1; i++) {
       pairs.push({ from: agentConfigs[i], to: agentConfigs[i+1] });
    }
    // Cross connections for consensus
    pairs.push({ from: agentConfigs[1], to: agentConfigs[5] }); // Architect -> Critic
    pairs.push({ from: agentConfigs[5], to: agentConfigs[2] }); // Critic -> Engineer
    pairs.push({ from: agentConfigs[3], to: agentConfigs[4] }); // Executor -> Evaluator
    return pairs;
  }, []);

  return (
    <group>
      {connections.map((conn, i) => {
        const fromActive = agents[conn.from.name]?.status !== "IDLE" && agents[conn.from.name]?.status !== "COMPLETED";
        const toActive = agents[conn.to.name]?.status !== "IDLE" && agents[conn.to.name]?.status !== "COMPLETED";
        
        return (
          <Connection 
            key={i} 
            start={conn.from.pos} 
            end={conn.to.pos} 
            color={conn.from.color} 
            isActive={fromActive || toActive} 
          />
        );
      })}
    </group>
  );
};
