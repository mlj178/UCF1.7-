public class InvincibleBuff : Buff
{
	public bool ignoreAttack;

	public InvincibleBuff(string name, float duration, Entity owner)
		: base(null, 0f, null)
	{
	}

	private void Owner_Invincible_BuffUpdater(ref bool value)
	{
	}

	protected override void OnLifeEnd()
	{
	}
}
