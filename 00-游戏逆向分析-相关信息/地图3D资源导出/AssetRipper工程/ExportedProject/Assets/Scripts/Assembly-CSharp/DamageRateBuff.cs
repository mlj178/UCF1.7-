public class DamageRateBuff : Buff
{
	public float damageRate;

	public DamageRateBuff(string name, float duration, Entity owner, float rate)
		: base(null, 0f, null)
	{
	}

	private void DamageRateBuffUpdate(ref float damageUp, ref float damageDown)
	{
	}

	protected override void OnLifeEnd()
	{
	}
}
