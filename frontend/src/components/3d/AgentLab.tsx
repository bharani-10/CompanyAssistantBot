import React, { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import * as THREE from 'three';
import { OrbitControls, Stars, PerspectiveCamera, Environment, ContactShadows } from '@react-three/drei';
import { Bloom, EffectComposer, Noise, Vignette, ChromaticAberration } from '@react-three/postprocessing';
import { AgentNode } from './AgentNode';
import { NeuralConnections } from './NeuralConnections';
import { useMetaMindStore } from '../../store/useMetaMindStore';

export const AgentLab: React.FC = () => {
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

  return (
    <div className="w-full h-full">
      <Canvas shadows dpr={[1, 2]}>
        <PerspectiveCamera makeDefault position={[0, 0, 12]} fov={50} />
        
        <color attach="background" args={["#020617"]} />
        <fog attach="fog" args={["#020617", 10, 25]} />
        
        <ambientLight intensity={0.2} />
        <pointLight position={[10, 10, 10]} intensity={1.5} color="#3b82f6" />
        <pointLight position={[-10, -10, -10]} intensity={1.5} color="#7000ff" />

        <Suspense fallback={null}>
          <group position={[0, -0.5, 0]}>
            <NeuralConnections />
            {agentConfigs.map((config) => {
              const agentState = agents[config.name];
              const isActive = agentState?.status !== "IDLE" && agentState?.status !== "COMPLETED";
              
              return (
                <AgentNode 
                  key={config.name}
                  name={config.name}
                  position={config.pos as [number, number, number]}
                  color={config.color}
                  status={agentState?.status || "IDLE"}
                  isActive={isActive}
                />
              );
            })}
          </group>

          <Stars 
            radius={150} 
            depth={60} 
            count={10000} 
            factor={6} 
            saturation={0.5} 
            fade 
            speed={2} 
          />
          
          <mesh rotation-x={-Math.PI / 2} position={[0, -4, 0]} receiveShadow>
            <planeGeometry args={[100, 100]} />
            <meshStandardMaterial color="#050510" roughness={0.8} metalness={0.2} />
          </mesh>
          
          <ContactShadows opacity={0.4} scale={20} blur={24} far={10} resolution={256} color="#000000" />
        </Suspense>

        <OrbitControls 
          enablePan={false} 
          minDistance={5} 
          maxDistance={20}
          maxPolarAngle={Math.PI / 1.8}
        />

        <EffectComposer disableNormalPass>
          <Bloom 
            luminanceThreshold={1.2} 
            mipmapBlur 
            intensity={1.5} 
            radius={0.4} 
          />
          <ChromaticAberration
            offset={new THREE.Vector2(0.0015, 0.0015)}
          />
          <Noise opacity={0.05} />
          <Vignette eskil={false} offset={0.1} darkness={1.1} />
        </EffectComposer>
      </Canvas>
    </div>
  );
};
