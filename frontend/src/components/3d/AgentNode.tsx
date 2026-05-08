import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Float, Text, MeshDistortMaterial, Sphere } from '@react-three/drei';
import * as THREE from 'three';

interface AgentNodeProps {
  name: string;
  position: [number, number, number];
  color: string;
  status: string;
  isActive: boolean;
}

export const AgentNode: React.FC<AgentNodeProps> = ({ name, position, color, status, isActive }) => {
  const meshRef = useRef<THREE.Group>(null);
  const ringRef = useRef<THREE.Mesh>(null);
  const coreRef = useRef<THREE.Mesh>(null);

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.getElapsedTime() * 0.5;
    }
    if (ringRef.current) {
      ringRef.current.rotation.x = state.clock.getElapsedTime() * 2;
      ringRef.current.rotation.y = state.clock.getElapsedTime() * 1.5;
    }
    if (isActive && coreRef.current) {
      const scale = 1 + Math.sin(state.clock.getElapsedTime() * 10) * 0.15;
      coreRef.current.scale.setScalar(scale);
    }
  });

  return (
    <Float speed={isActive ? 5 : 1} rotationIntensity={isActive ? 2 : 0.5} floatIntensity={isActive ? 2 : 0.5} position={position}>
      <group ref={meshRef}>
        {/* Pulsing Energy Core */}
        <mesh ref={coreRef}>
          <sphereGeometry args={[0.6, 32, 32]} />
          <MeshDistortMaterial 
            color={color} 
            speed={isActive ? 5 : 1} 
            distort={isActive ? 0.4 : 0.2} 
            emissive={color}
            emissiveIntensity={isActive ? 2 : 0.5}
            transparent
            opacity={0.9}
          />
        </mesh>

        {/* Global Orbital Ring */}
        <mesh ref={ringRef}>
          <torusGeometry args={[0.9, 0.02, 16, 100]} />
          <meshStandardMaterial 
            color={color} 
            emissive={color} 
            emissiveIntensity={isActive ? 5 : 0.5} 
            toneMapped={false} 
          />
        </mesh>

        {/* Outer Halo */}
        <mesh scale={[1.2, 1.2, 1.2]}>
          <sphereGeometry args={[0.7, 32, 32]} />
          <meshStandardMaterial 
            color={color} 
            transparent 
            opacity={isActive ? 0.1 : 0.02} 
            wireframe 
          />
        </mesh>
      </group>

      <Text
        position={[0, 1.2, 0]}
        fontSize={0.22}
        color="white"
        font="/fonts/Inter-Bold.woff"
        anchorX="center"
        anchorY="middle"
      >
        {name.toUpperCase()}
      </Text>
      
      <Text
        position={[0, -1, 0]}
        fontSize={0.12}
        color={isActive ? color : "#666"}
        font="/fonts/Inter-Medium.woff"
        anchorX="center"
        anchorY="middle"
      >
        {status.toUpperCase()}
      </Text>
    </Float>
  );
};
