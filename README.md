# Hanoi Tower

## Auteurs

- Zakaria Maanane
- Sewa Fumey

---

## Introduction

**How do you know when the Hanoi Tower is lying ?  
Its story doesn't stack up !**

Ce projet consiste à développer une version automatisée du jeu de réflexion **Tour de Hanoï**, dans laquelle une **IA** résout seule la partie en utilisant le principe de **récursivité**.

---

## Problématique

Les Tours de Hanoï sont un jeu de réflexion imaginé par Édouard Lucas.  
Le but est de déplacer des disques de diamètres différents d’une tour de départ à une tour d’arrivée en passant éventuellement par une tour intermédiaire, et ceci en un **minimum de déplacements**.

Règles :
- On ne peut bouger qu’un disque à la fois.
- Un disque plus grand ne peut jamais être placé sur un plus petit.

---

## Solution proposée

Nous avons développé un outil complet pour résoudre et visualiser le jeu grâce à une IA récursive.

### Fonctionnalités

✔ Recevoir en entrée une configuration de partie sous forme de chaîne de caractères, par exemple :
