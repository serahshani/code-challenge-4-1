from random import choice as rc
from app import app
from models import db, Hero, Power, HeroPower

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        HeroPower.query.delete()  # Delete HeroPower first due to foreign key constraints
        Power.query.delete()
        Hero.query.delete()

        print("Seeding powers...")
        powers = [
            Power(name="super strength", description="Gives the wielder super-human strength to perform extraordinary feats."),
            Power(name="flight", description="Gives the wielder the ability to fly through the skies at supersonic speed."),
            Power(name="super human senses", description="Allows the wielder to use her senses at a super-human level, detecting dangers."),
            Power(name="elasticity", description="Can stretch the human body to extreme lengths, enabling incredible flexibility."),
        ]

        db.session.add_all(powers)

        print("Seeding heroes...")
        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra"),
        ]

        db.session.add_all(heroes)

        print("Adding powers to heroes...")
        strengths = ["Strong", "Weak", "Average"]
        hero_powers = []
        for hero in heroes:
            power = rc(powers)
            hero_powers.append(
                HeroPower(hero=hero, power=power, strength=rc(strengths))
            )
        db.session.add_all(hero_powers)

        # Commit changes to the database
        db.session.commit()

        print("Done seeding!")
