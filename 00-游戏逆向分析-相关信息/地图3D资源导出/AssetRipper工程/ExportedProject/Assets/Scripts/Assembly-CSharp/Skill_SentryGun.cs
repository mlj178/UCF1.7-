using System;

public class Skill_SentryGun : Skill_Common
{
	private SentryGun bindSentry;

	public Skill_SentryGun(string name, Func<Player, bool> workFunction, float coldTime)
		: base(null, null, 0f)
	{
	}

	public void BindSentry(SentryGun sentry)
	{
	}

	public bool IsNoneSentryGun()
	{
		return false;
	}
}
