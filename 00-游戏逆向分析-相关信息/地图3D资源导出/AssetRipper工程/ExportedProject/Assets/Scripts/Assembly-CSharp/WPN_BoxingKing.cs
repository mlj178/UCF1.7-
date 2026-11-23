public class WPN_BoxingKing : WPN_Knife
{
	private float landCheckStartTime;

	private Skill_Common kickSkill;

	private Skill_Common rotateSkill;

	private Skill_Common flySkill;

	private bool isRotating;

	private bool isFlying;

	public override void Init()
	{
	}

	protected override void SetValidOwner()
	{
	}

	protected override void RemoveFromOldOwner()
	{
	}

	public override void Deploy(bool noSelectAnim = false)
	{
	}

	protected override void Update()
	{
	}

	private bool Kick(Player player)
	{
		return false;
	}

	private bool Rotate(Player player)
	{
		return false;
	}

	private bool Fly(Player player)
	{
		return false;
	}
}
