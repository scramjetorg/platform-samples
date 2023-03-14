export type CharacterType = {
    spec: "wizard" | "warrior";
    weapon: string;
    hp: string;
    spell?: string;
};

export interface CharacterInterface {
    spec: CharacterType["spec"];
    weapon: string;
    hp: string;
    spell?: string;
    getSpec(): string;
    getWeapon(): string;
    getHp(): string;
    toString(): string;
    message(): string;
}

export abstract class Character implements CharacterInterface {
    spec: CharacterType["spec"];
    weapon: string;
    hp: string;
    spell?: string;

    constructor(info: CharacterType) {
        this.spec = info.spec;
        this.weapon = info.weapon;
        this.hp = info.hp;
        this.spell = info.spell;
    }

    getSpec() {
        return this.spec;
    }

    getWeapon() {
        return this.weapon;
    }

    getHp() {
        return this.hp;
    }

    abstract toString(): string;
    abstract message(): string;
}
